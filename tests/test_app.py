def test_se_a_pagina_inicial_retorna_status_code_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_se_retorna_status_code_401_para_usuario_nao_autorizado(client):
    response = client.get('/lista_alunos')
    assert response.status_code == 401

def test_se_o_link_entrar_existe_no_menu(client):
    response = client.get('/')
    assert "Entrar" in response.get_data(as_text=True)

def test_se_a_pagina_entrar_retorna_status_code_200(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_se_consegue_cadastrar_novo_usuario(client):
    data = {
        "nome":"robocop",
        "senha":"123",
        "email":"robocop@usuario"
    }
    response = client.post('/cadastrar_usuario', data=data, follow_redirects=True)    
    assert "robocop" in response.get_data(as_text=True)

def test_se_o_usuario_consegue_conectar(client):
    data = {
        "nome":"robocop",
        "senha":"123",
        "email":"robocop@usuario"
    }
    response = client.post('/cadastrar_usuario', data=data, follow_redirects=True)
    response = client.post('/login', data=data, follow_redirects=True)
    assert "web em Flask" in response.get_data(as_text=True)

def test_se_o_link_sair_existe_no_menu(client):
    data = {
        "nome":"robocop",
        "senha":"123",
        "email":"robocop@usuario"
    }
    response = client.post('/cadastrar_usuario', data=data, follow_redirects=True)
    response = client.post('/login', data=data, follow_redirects=True)
    assert "Sair" in response.get_data(as_text=True) 
   
def test_se_botoes_cadastrar_usuario_e_editar_e_excluir_existem(client):
    data = {
        "nome":"robocop",
        "senha":"123",
        "email":"robocop@usuario"
    }
    response = client.post('/cadastrar_usuario', data=data, follow_redirects=True)
    response = client.post('/login', data=data, follow_redirects=True)
    response = client.get('/lista_usuarios')
    assert "Excluir" in response.get_data(as_text=True)
    assert "Editar" in response.get_data(as_text=True)
    assert "Cadastrar Usuário" in response.get_data(as_text=True)

def test_acessar_pagina_para_editar_dados_do_usuario(client):
    data = {
        "nome":"robocop",
        "senha":"123",
        "email":"robocop@usuario"
    }
    response = client.post('/cadastrar_usuario', data=data, follow_redirects=True)
    response = client.post('/login', data=data, follow_redirects=True)
    response = client.get('/1/atualiza_usuario')
    assert "Atualizar dados do usuário robocop" in response.get_data(as_text=True)
