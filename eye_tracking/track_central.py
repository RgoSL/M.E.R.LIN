# Classe Para Controlar o Acesso a Camera e Distribuir Detecções Entre Todos as Outras

import threading
import time
import cv2
import mediapipe as mp
from queue import Queue, Empty

class GerenciadorCamera:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.camera_ativa = False
        self.cap = None
        self.frame_atual = None
        self.resultado_atual = None
        
        # Aplicação dos Métodos de Detecção de Rosto do MediaPipe
        self.mp_face = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        
        # Janelas com Código OpenCV
        self.clientes = {}  # Recebem um ID e um Estado de Necessidade Para Receber os Dados Dessa Classe
        self.lock_clientes = threading.Lock()
        
        # Thread de Captura
        self.thread_captura = None
        self.thread_processamento = None
        self.executando = False
        
        # Configurações
        self.cam_index = 0
        self.fps_target = 30
        self.mostrar_debug = False
    
    def iniciar(self, cam_index=0, mostrar_debug=False):
        # Boot de Captura
        if self.camera_ativa:
            return True
        
        self.cam_index = cam_index
        self.mostrar_debug = mostrar_debug
        
        try:
            self.cap = cv2.VideoCapture(self.cam_index)
            if not self.cap.isOpened():
                print("❌ Erro: Não foi possível abrir a câmera")
                return False
            
            # Configuração da Resolução Capturada
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.camera_ativa = True
            self.executando = True
            
            # Boot de Threads
            self.thread_captura = threading.Thread(
                target=self._loop_captura,
                daemon=True
            )
            self.thread_processamento = threading.Thread(
                target=self._loop_processamento,
                daemon=True
            )
            
            self.thread_captura.start()
            self.thread_processamento.start()
            
            print("Câmera inicializada")
            return True
            
        except Exception as e:
            print(f"Erro ao iniciar câmera: {e}")
            return False
    
    def parar(self):
        # Para o Uso da Camera
        if not self.camera_ativa:
            return
        
        self.executando = False
        self.camera_ativa = False
        
        # Ativação Controlada Das Threads
        if self.thread_captura:
            self.thread_captura.join(timeout=1.0)
        if self.thread_processamento:
            self.thread_processamento.join(timeout=1.0)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        if self.mostrar_debug:
            cv2.destroyAllWindows()
        
        print("Câmera desligada")
    
    def registrar_cliente(self, id_cliente, callback, ativo=True):
        # Elementos Integrados(Dock, Teclado e ListaApps) São Referidos Como Clientes

        with self.lock_clientes:
            self.clientes[id_cliente] = {
                "callback": callback,
                "ativo": ativo
            }
        # Boot da Camera
        if not self.camera_ativa:
            self.iniciar(mostrar_debug=self.mostrar_debug)
        
        print(f"✓ Cliente '{id_cliente}' registrado")
    
    def remover_cliente(self, id_cliente):
        # Remove Algum Elemento Integrado
        with self.lock_clientes:
            if id_cliente in self.clientes:
                del self.clientes[id_cliente]
                print(f"✓ Cliente '{id_cliente}' removido")
        
        # Encerra o Uso da Camera
        if len(self.clientes) == 0:
            self.parar()
    
    def ativar_cliente(self, id_cliente):
        # Ativa Algum Elemento Integrado
        with self.lock_clientes:
            if id_cliente in self.clientes:
                self.clientes[id_cliente]["ativo"] = True
                print(f"✓ Cliente '{id_cliente}' ativado")
    
    def desativar_cliente(self, id_cliente):
        # Desativa Algum Elemento Integrado
        with self.lock_clientes:
            if id_cliente in self.clientes:
                self.clientes[id_cliente]["ativo"] = False
                print(f"✓ Cliente '{id_cliente}' desativado")
    
    def _loop_captura(self):
        # Thread Para Capturas FPS
        intervalo = 1.0 / self.fps_target
        
        while self.executando:
            inicio = time.time()
            
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    self.frame_atual = cv2.flip(frame, 1)
            
            # Mantém FPS
            tempo_decorrido = time.time() - inicio
            if tempo_decorrido < intervalo:
                time.sleep(intervalo - tempo_decorrido)
    
    def _loop_processamento(self):
        # Threads de Detecção e Processamento
        while self.executando:
            if self.frame_atual is None:
                time.sleep(0.01)
                continue
            
            frame = self.frame_atual.copy()
            h, w, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.mp_face.process(rgb_frame)
            
            # Montando a Forma Como os Resultados São Enviados
            resultado = {
                "frame": frame,
                "landmarks": None,
                "width": w,
                "height": h,
                "timestamp": time.time()
            }
            
            if results.multi_face_landmarks:
                resultado["landmarks"] = results.multi_face_landmarks[0].landmark
            
            self.resultado_atual = resultado
            
            self._notificar_clientes(resultado)
            
            if self.mostrar_debug:
                self._mostrar_debug(frame, results)
            
            time.sleep(0.01)
    
    def _notificar_clientes(self, resultado):
        # Envia os Resultados Para as Classes Dos Elementos
        with self.lock_clientes:
            for id_cliente, cliente in self.clientes.items():
                if cliente["ativo"]:
                    try:
                        cliente["callback"](resultado)
                    except Exception as e:
                        print(f"Erro no callback de '{id_cliente}': {e}")
    
    def _mostrar_debug(self, frame, results):
        #Ativa as Janelas Para Debug
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            h, w, _ = frame.shape
            
            # Cria os Desenhos Das Landmarks
            LEFT_EYE = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE = [362, 385, 387, 263, 373, 380]
            
            for idx in LEFT_EYE + RIGHT_EYE:
                x = int(landmarks[idx].x * w)
                y = int(landmarks[idx].y * h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        
        # Mostra os Elementos Integrados Ativos
        with self.lock_clientes:
            clientes_ativos = [id_c for id_c, c in self.clientes.items() if c["ativo"]]
        
        texto = f"Clientes: {', '.join(clientes_ativos) if clientes_ativos else 'Nenhum'}"
        cv2.putText(frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, (0, 255, 0), 2)
        
        cv2.imshow("M.E.R.LIN - Debug Camera", frame)
        cv2.waitKey(1)


# Para Facilar a Instância 
gerenciador = GerenciadorCamera()

def eye_aspect_ratio(landmarks, eye_indices, w, h):
    # Cálculo com Método EAR
    coords = [
        (int(landmarks[i].x * w), int(landmarks[i].y * h))
        for i in eye_indices
    ]
    
    A = ((coords[1][1] - coords[5][1])**2 + (coords[1][0] - coords[5][0])**2)**0.5
    B = ((coords[2][1] - coords[4][1])**2 + (coords[2][0] - coords[4][0])**2)**0.5
    C = ((coords[0][1] - coords[3][1])**2 + (coords[0][0] - coords[3][0])**2)**0.5
    
    return (A + B) / (2.0 * C) if C != 0 else 1.0


def calcular_posicao_nariz(landmarks, w, h):
    # Para Padronizar a Posição do Nariz 
    if landmarks is None:
        return 0.5
    
    return landmarks[1].x