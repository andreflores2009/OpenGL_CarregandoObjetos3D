# Luzes

# Neste exemplo, especificamos uma uma iluminação ambiente, difusa e especular básicas.
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from TextureLoader import load_texture
from ObjLoader import ObjLoader
from Camera import Camera
import pyrr

Window = None
Shader_programm = None

Vao_Objeto = None
obj_indices = None
obj_buffer = None
obj_textura = None

WIDTH = 800
HEIGHT = 600

Tempo_entre_frames = 0 #variavel utilizada para movimentar a camera

#Variáveis referentes a luz1
luz_posicao1 = pyrr.Vector3([-10.0, 0.0, 0.0])
La1 = pyrr.Vector3([0.2, 0.2, 0.2]) #Luz ambiente
Ld1 = pyrr.Vector3([1.0, 0.0, 0.0]) #Luz Vermelha
Ls1 = pyrr.Vector3([1.0, 0.0, 0.0]) #luz vermelha

#Variáveis referentes a luz2
luz_posicao2 = pyrr.Vector3([10.0, 0.0, 0.0])
La2 = pyrr.Vector3([0.5, 0.2, 0.2]) #Luz ambiente
Ld2 = pyrr.Vector3([0.0, 0.0, 1.0]) #luz azul
Ls2 = pyrr.Vector3([0.0, 0.0, 1.0]) #luz azul


luz_speed = 50.0 #velocidade da luz qdo movimentada pelo teclado, 1 unidade por segundo

cam = Camera()

lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False

def redimensionaCallback(window, w, h):
    global WIDTH, HEIGHT
    WIDTH = w
    HEIGHT = h

def tecladoCallback(window, key, scancode, action, mode):
    global left, right, forward, backward, Tempo_entre_frames, luz_posicao1
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False
    # if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
    #     left, right, forward, backward = False, False, False, False

    #parâmetros da posição da luz
    if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_KP_4)):
        luz_posicao1[0] -= luz_speed * Tempo_entre_frames
    if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_KP_6)):
        luz_posicao1[0] += luz_speed * Tempo_entre_frames

    if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_KP_5)):
        luz_posicao1[1] -= luz_speed * Tempo_entre_frames
    if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_KP_8)):
        luz_posicao1[1] += luz_speed * Tempo_entre_frames

    if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_KP_7)):
        luz_posicao1[2] -= luz_speed * Tempo_entre_frames
    if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_KP_9)):
        luz_posicao1[2] += luz_speed * Tempo_entre_frames

def mouseCallback(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def movimentaCamera():
    if left:
        cam.process_keyboard("LEFT", 0.05)
    if right:
        cam.process_keyboard("RIGHT", 0.05)
    if forward:
        cam.process_keyboard("FORWARD", 0.05)
    if backward:
        cam.process_keyboard("BACKWARD", 0.05)

def inicializaOpenGL():
    global Window, WIDTH, HEIGHT

    #Inicializa GLFW
    glfw.init()

    #Criação de uma janela
    Window = glfw.create_window(WIDTH, HEIGHT, "Exemplo - renderização de um triângulo", None, None)
    if not Window:
        glfw.terminate()
        exit()

    glfw.set_window_size_callback(Window, redimensionaCallback) #função callback de redimensionamento
    glfw.set_key_callback(Window, tecladoCallback) #função callback do teclado
    glfw.set_cursor_pos_callback(Window, mouseCallback) #função callback do mouse
    glfw.set_input_mode(Window, glfw.CURSOR, glfw.CURSOR_DISABLED) #desabilita o cursor
    glfw.make_context_current(Window)

    print("Placa de vídeo: ",OpenGL.GL.glGetString(OpenGL.GL.GL_RENDERER))
    print("Versão do OpenGL: ",OpenGL.GL.glGetString(OpenGL.GL.GL_VERSION))

def inicializaObjeto():
    global Vao_Objeto, obj_buffer, obj_indices, obj_textura
    obj_indices, obj_buffer = ObjLoader.load_model("meshes/chibi.obj")

    #Vao do objeto
    Vao_Objeto = glGenVertexArrays(1)
    glBindVertexArray(Vao_Objeto)

    #VBO do objeto. Ao invés de termos 1 VBO para cada informação (vértices, texturas, normais, etc.), este exemplo utiliza
    #1 único VBO com todas as informações dentro
    bvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, bvbo)
    glBufferData(GL_ARRAY_BUFFER, obj_buffer.nbytes, obj_buffer, GL_STATIC_DRAW)
    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj_buffer.itemsize * 8, ctypes.c_void_p(0))
    # texturas
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj_buffer.itemsize * 8, ctypes.c_void_p(12))
    # normais
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    #carrega os arquivos de textura
    obj_textura = glGenTextures(1)
    load_texture("textures/chibi.png", obj_textura)

def inicializaShaders():
    global Shader_programm
    # Especificação do Vertex Shader:
    vertex_shader = """
        #version 400
        layout(location = 0) in vec3 vertex_posicao; //vértices do objeto vindas do modelo do objeto (PYTHON)
        layout(location = 1) in vec2 vertex_texture; //normais do objeto vindas do modelo do objeto (PYTHON)
        layout(location = 2) in vec3 vertex_normal; //normais do objeto vindas do modelo do objeto (PYTHON)
        out vec3 vertex_posicao_cam, vertex_normal_cam;
        out vec2 v_texture; //saida da textura para o fragment shader
        uniform mat4 transform, view, proj;
        void main () {
            vertex_posicao_cam = vec3 (view * transform * vec4 (vertex_posicao, 1.0)); //posição do objeto em relação a CÂMERA
            vertex_normal_cam = vec3 (view *  transform * vec4 (vertex_normal, 0.0)); //normais do objeto em relação a CÂMERA

            v_texture = vertex_texture;

            gl_Position = proj * view * transform * vec4 (vertex_posicao, 1.0);
        }
    """
    vs = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        infoLog = glGetShaderInfoLog(vs, 512, None)
        print("Erro no vertex shader:\n", infoLog)

    # Especificação do Fragment Shader:
    fragment_shader = """
        #version 400
		in vec3 vertex_posicao_cam, vertex_normal_cam; //variáveis vindas do VERTEX SHADER
        in vec2 v_texture; //variável de textura vinda do VERTEX SHADER
        uniform sampler2D s_texture;
        
        //propriedades de uma luz pontual 1
        uniform vec3 luz_posicao1;
        uniform vec3 Ls1;// luz especular
		uniform vec3 Ld1;// luz difusa
		uniform vec3 La1;// luz ambiente

        //propriedades de uma luz pontual 2
        uniform vec3 luz_posicao2;
        uniform vec3 Ls2;// luz especular
		uniform vec3 Ld2;// luz difusa
		uniform vec3 La2;// luz ambiente

        //propriedades de reflexão da superficie do objeto vindas do PYTHON
		uniform vec3 Ks;//reflexão especular
		uniform vec3 Kd;//reflexão difusa
		uniform vec3 Ka;//reflexão ambiente
        uniform float especular_exp;//expoente especular
        
        uniform mat4 view; //matriz da câmera vinda do PYTHON
		out vec4 frag_colour;

        //variáveis globais que são utilizadas tanto na intensidade difusa quanto especular, para não precisar recalcular duas vezes
        vec3 vertex_normal_cam_normalizada;
        vec3 luz_posicao_cam1, luz_vetor_cam1, luz_vetor_cam_normalizada1; //da luz 1
        vec3 luz_posicao_cam2, luz_vetor_cam2, luz_vetor_cam_normalizada2; //da luz 2

        vec3 intensidadeAmbiente1(){
            vec3 Ia = La1 * Ka;
            return Ia;
        }

        vec3 intensidadeAmbiente2(){
            vec3 Ia = La2 * Ka;
            return Ia;
        }

        vec3 intensidadeDifusa1(){
            luz_posicao_cam1 = vec3 (view * vec4 (luz_posicao1, 1.0));//posicao da luz em relação a câmera
            luz_vetor_cam1 = luz_posicao_cam1 - vertex_posicao_cam;//vetor apontando para a luz em relação a posicao do vértice 
            luz_vetor_cam_normalizada1 = normalize(luz_vetor_cam1);//vetor da luz normalizada
            vertex_normal_cam_normalizada = normalize(vertex_normal_cam);
            float cosseno_difusa = dot(vertex_normal_cam_normalizada,luz_vetor_cam_normalizada1);//cosseno do angulo entre o vetor da luz e a normal da superficie
            
            vec3 Id = Ld1 * Kd * cosseno_difusa;
            return Id;

        }

        vec3 intensidadeDifusa2(){
            luz_posicao_cam2 = vec3 (view * vec4 (luz_posicao2, 1.0));//posicao da luz em relação a câmera
            luz_vetor_cam2 = luz_posicao_cam2 - vertex_posicao_cam;//vetor apontando para a luz em relação a posicao do vértice
            luz_vetor_cam_normalizada2 = normalize(luz_vetor_cam2);//vetor da luz normalizada
            vertex_normal_cam_normalizada = normalize(vertex_normal_cam);
            float cosseno_difusa = dot(vertex_normal_cam_normalizada,luz_vetor_cam_normalizada2);//cosseno do angulo entre o vetor da luz e a normal da superficie
            
            vec3 Id = Ld2 * Kd * cosseno_difusa;

            return Id;

        }

        vec3 intensidadeEspecular1(){
            vec3 luz_reflexao_vetor_cam = reflect(-luz_vetor_cam_normalizada1, vertex_normal_cam_normalizada);
            vec3 superficie_camera_vetor = normalize(-vertex_posicao_cam);
            float cosseno_especular = dot(luz_reflexao_vetor_cam, superficie_camera_vetor);
            cosseno_especular = max(cosseno_especular, 0.0);//se o cosseno der negativo, atribui 0 para ele
            float fator_especular = pow (cosseno_especular, especular_exp);

            vec3 Is = Ls1 * Ks * fator_especular;

            return Is;
        }

        vec3 intensidadeEspecular2(){
            vec3 luz_reflexao_vetor_cam = reflect(-luz_vetor_cam_normalizada2, vertex_normal_cam_normalizada);
            vec3 superficie_camera_vetor = normalize(-vertex_posicao_cam);
            float cosseno_especular = dot(luz_reflexao_vetor_cam, superficie_camera_vetor);
            cosseno_especular = max(cosseno_especular, 0.0);//se o cosseno der negativo, atribui 0 para ele
            float fator_especular = pow (cosseno_especular, especular_exp);

            vec3 Is = Ls1 * Ks * fator_especular;

            return Is;
        }
		void main () {

            vec3 Ia1 = intensidadeAmbiente1();
            vec3 Ia2 = intensidadeAmbiente2();

            vec3 Id1 = intensidadeDifusa1();
            vec3 Id2 = intensidadeDifusa2();

            vec3 Is1 = intensidadeEspecular1();
            vec3 Is2 = intensidadeEspecular2();

            vec4 corReflexao = vec4(Ia1+Ia2+Id1+Id2+Is1+Is2, 1.0);
            vec4 corTextura = texture(s_texture, v_texture);

            /*A cor final do fragmento é a soma das 3 componentes de iluminação + cor da textura*/
            frag_colour = corReflexao + corTextura;
		}
    """
    fs = OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        infoLog = glGetShaderInfoLog(fs, 512, None)
        print("Erro no fragment shader:\n", infoLog)

    # Especificação do Shader Programm:
    Shader_programm = OpenGL.GL.shaders.compileProgram(vs, fs)
    if not glGetProgramiv(Shader_programm, GL_LINK_STATUS):
        infoLog = glGetProgramInfoLog(Shader_programm, 512, None)
        print("Erro na linkagem do shader:\n", infoLog)

    glDeleteShader(vs)
    glDeleteShader(fs)

def transformacaoGenerica(Tx, Ty, Tz, Sx, Sy, Sz, Rx, Ry, Rz):

    #matriz de translação
    translacao = pyrr.matrix44.create_from_translation(pyrr.Vector3([Tx, Ty, Tz]))

    #matriz de rotação em torno do eixo X
    anguloX = np.radians(Rx)
    rotacaoX = pyrr.matrix44.create_from_x_rotation(anguloX)

    #matriz de rotação em torno do eixo Y
    anguloY = np.radians(Ry)
    rotacaoY = pyrr.matrix44.create_from_y_rotation(anguloY)

    #matriz de rotação em torno do eixo Z
    anguloZ = np.radians(Rz)
    rotacaoZ = pyrr.matrix44.create_from_z_rotation(anguloZ)

    #combinação das 3 rotação
    rotacao = pyrr.matrix44.multiply(rotacaoY, rotacaoX)
    rotacao = pyrr.matrix44.multiply(rotacaoZ, rotacao)

    #matriz de escala
    escala = pyrr.matrix44.create_from_scale(pyrr.Vector3([Sx, Sy, Sz]))

    transformacaoFinal = pyrr.matrix44.multiply(rotacao, escala)
    transformacaoFinal = pyrr.matrix44.multiply(translacao, transformacaoFinal)
    
    #E passamos a matriz para o Vertex Shader.
    transformLoc = glGetUniformLocation(Shader_programm, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, transformacaoFinal)

def especificaMatrizVisualizacao():
    visualizacao = cam.get_view_matrix()
    transformLoc = glGetUniformLocation(Shader_programm, "view")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, visualizacao)

def especificaMatrizProjecao():
    #Especificação da matriz de projeção perspectiva.
    projecao = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
    transformLoc = glGetUniformLocation(Shader_programm, "proj")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, projecao)

def inicializaCamera():
    especificaMatrizVisualizacao()
    especificaMatrizProjecao()


def especificaMaterial(KaR, KaG, KaB, KdR, KdG, KdB, KsR, KsG, KsB, n):
    global Shader_programm
    #Coeficiente de reflexão ambiente
    Ka = pyrr.Vector3([KaR, KaG, KaB])#reflete luz ambiente
    Ka_loc = glGetUniformLocation(Shader_programm, "Ka")
    glUniform3fv(Ka_loc, 1, Ka)

    #Coeficiente de reflexão difusa
    Kd = pyrr.Vector3([KdR, KdG, KdB])#reflete luz difusa
    Kd_loc = glGetUniformLocation(Shader_programm, "Kd")
    glUniform3fv(Kd_loc, 1, Kd)

    #Coeficiente de reflexão especular
    Ks = pyrr.Vector3([KsR, KsG, KsB])#reflete luz especular
    Ks_loc = glGetUniformLocation(Shader_programm, "Ks")
    glUniform3fv(Ks_loc, 1, Ks)

    #expoente expecular
    especular_exp = n
    especular_exp_loc = glGetUniformLocation(Shader_programm, "especular_exp")
    glUniform1f(especular_exp_loc, especular_exp)

def especificaLuz1():
    global Shader_programm, luz_posicao1, La1, Ld1, Ls1
    #posição da luz
    luz_posicaoloc = glGetUniformLocation(Shader_programm, "luz_posicao1")#envia o array da posição da luz para o shader
    glUniform3fv(luz_posicaoloc, 1, luz_posicao1)

    #Fonte de luz ambiente
    La_loc = glGetUniformLocation(Shader_programm, "La1")#envia o array da Luz Ambiente para o shader
    glUniform3fv(La_loc, 1, La1)

    #Fonte de luz difusa
    Ld_loc = glGetUniformLocation(Shader_programm, "Ld1")#envia o array da Luz Difusa para o shader
    glUniform3fv(Ld_loc, 1, Ld1)
    
    #Fonte de luz especular
    Ls_loc = glGetUniformLocation(Shader_programm, "Ls1")#envia o array da Luz Especular para o shader
    glUniform3fv(Ls_loc, 1, Ls1)

def especificaLuz2():
    global Shader_programm, luz_posicao2, La2, Ld2, Ls2
    #posição da luz
    luz_posicaoloc = glGetUniformLocation(Shader_programm, "luz_posicao2")#envia o array da posição da luz para o shader
    glUniform3fv(luz_posicaoloc, 1, luz_posicao2)

    #Fonte de luz ambiente
    La_loc = glGetUniformLocation(Shader_programm, "La2")#envia o array da Luz Ambiente para o shader
    glUniform3fv(La_loc, 1, La2)

    #Fonte de luz difusa
    Ld_loc = glGetUniformLocation(Shader_programm, "Ld2")#envia o array da Luz Difusa para o shader
    glUniform3fv(Ld_loc, 1, Ld2)
    
    #Fonte de luz especular
    Ls_loc = glGetUniformLocation(Shader_programm, "Ls2")#envia o array da Luz Especular para o shader
    glUniform3fv(Ls_loc, 1, Ls2)

def inicializaRenderizacao():
    global Window, Shader_programm, Vao, WIDTH, HEIGHT, Tempo_entre_frames

    tempo_anterior = glfw.get_time()

    #Ativação do teste de profundidade. Sem ele, o OpenGL não sabe que faces devem ficar na frente e que faces devem ficar atrás.
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while not glfw.window_should_close(Window):
        #calcula quantos segundos se passaram entre um frame e outro
        tempo_frame_atual = glfw.get_time()
        Tempo_entre_frames = tempo_frame_atual - tempo_anterior
        tempo_anterior = tempo_frame_atual

        movimentaCamera()

        #limpa a tela e os buffers
        glClearColor(0.2, 0.3, 0.3, 1.0)        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #configura a viewport para pegar toda a janela
        glViewport(0, 0, WIDTH, HEIGHT)

        #ativa o shader
        glUseProgram(Shader_programm)

        especificaLuz1() #parâmetros da fonte de luz
        especificaLuz2() #parâmetros da fonte de luz
                                
        inicializaCamera()#configuramos a câmera
        glBindVertexArray(Vao_Objeto) #ativamos o objeto que queremos renderizar
        
        especificaMaterial(0.2, 0.2, 0.2, 0.8, 0.8, 0.8, 0.1, 0.1, 0.1, 32)
        transformacaoGenerica(0,0,0,1,1,1,0,0,0)
        glDrawArrays(GL_TRIANGLES, 0, len(obj_indices))

        glfw.poll_events()

        glfw.swap_buffers(Window)
    
    glfw.terminate()

# Função principal
def main():
    inicializaOpenGL()
    inicializaObjeto()
    inicializaShaders()
    inicializaRenderizacao()

if __name__ == "__main__":
    main()


# Luzes

# Neste exemplo, carregamos um objeto 3D a partir de um arquivo OBJ e implementamos iluminação
# avançada utilizando shaders customizados. O programa também permite controle interativo da câmera
# e das fontes de luz durante a renderização.

# Principais funcionalidades:
# - Carrega um modelo 3D (arquivo OBJ) e renderiza utilizando shaders personalizados.
# - Implementa iluminação ambiente, difusa e especular para duas fontes de luz.
# - Permite controle da posição das fontes de luz usando teclas específicas.
# - Inclui movimentação da câmera com teclado e rotação da visão com o mouse.
# - Utiliza matrizes de transformação para configurar a visualização e a projeção do objeto renderizado.

# Para isso, o código utiliza bibliotecas como PyOpenGL, GLFW, numpy e outras auxiliares para
# carregar modelos, texturas e controlar a câmera. A renderização é realizada em um loop principal
# que atualiza a posição das fontes de luz e da câmera, além de processar os inputs do teclado e mouse.


'''
Comparando este código com o Ex01 que você mencionou anteriormente, aqui estão algumas diferenças notáveis:

Iluminação e Shaders:
Neste código (Ex02), há a implementação completa de shaders (tanto o Vertex Shader quanto o Fragment Shader)
para lidar com iluminação ambiente, difusa e especular. No Ex01, o foco era principalmente na estruturação básica 
do OpenGL sem entrar em detalhes sobre iluminação e shaders.

Manipulação de Objetos:
No Ex02, há um objeto carregado a partir de um arquivo OBJ usando uma classe ObjLoader, 
o que permite trabalhar com objetos mais complexos. Isso adiciona uma camada de complexidade em 
comparação com o Ex01, que provavelmente tratava de renderização de geometrias mais simples.

Controle de Iluminação Dinâmica:
O Ex02 tem funcionalidades para controlar a posição das luzes interativamente (por meio do teclado),
 o que permite mover as fontes de luz durante a renderização. Isso não estava presente no Ex01,
 que provavelmente não tratava de iluminação dinâmica.

Uso de Bibliotecas Externas:
No Ex02, há referências a bibliotecas externas como pyrr (para manipulação de matrizes e vetores) 
e importações de módulos como TextureLoader e ObjLoader para lidar com texturas e carregar objetos 3D.
 O Ex01 poderia ter sido mais independente, sem dependências externas além do OpenGL.
'''