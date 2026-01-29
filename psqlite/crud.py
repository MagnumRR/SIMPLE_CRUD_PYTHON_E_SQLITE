# Utilizando o banco de dados presente no Python
# Importando o banco SQLite
# Instalando a biblioteca "tabulate" e importando-a
import sqlite3
from tabulate import tabulate

# Funcionalidade conexão com o banco
def conectar():
    '''Conexão com o banco'''
    # variável de conexão recebe o banco de dados de nome "bd_psqlite"
    conn = sqlite3.connect('bd_psqlite')
    
    # Processo para criação de uma tabela e campos
    conn.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL
    );
    """
    )
    return conn
    
# Funcionalidade desconectar banco de dados
def desconectar(conn):
    '''Desconectar do servidor.'''
    conn.close()

# Funcionalidade listando os registros de produtos
def listar():
    
    # Parametros de conexão
    conn = conectar()
    cursor = conn.cursor()
    
    # Consulta a tabela e listagem
    query = "SELECT * FROM produtos"
    cursor.execute(query)
    produtos = cursor.fetchall()
    headers = ['Id', 'Produto', 'Preço', 'Estoque']
    
    # Condição de exibição
    # Utilizando a biblioteca "Tabulate para estruturar os dados do banco, na forma de tabela,
    # para o usuário"
    print(f'---------- {len(produtos)} PRODUTOS -----------')
    if produtos:
        print(tabulate(produtos, headers=headers, tablefmt='simple'))
    else:
        print('\nSem produtos cadastrados.')    
    '''
    if produtos:
        print('ID ------ Produto -------- Preço ------ Qtd')  
        for i in produtos:
            print(f'{i[0]}         {i[1]}      {i[2]}        {i[3]}') 
    else:
        print('\nSem produtos cadastrados.')
    '''
    cursor.close()
    desconectar(conn)            
            
# Funcionalidade inserção de dados
def inserir():
    print('---------- NOVO PRODUTO -----------') 
    # Parâmetros de conexão
    conn = conectar()
    cursor = conn.cursor()
    
    # Entradas
    nome = input('Produto: ')
    preco = float(input('Valor: R$ '))
    estoque = int(input('Quantidade: '))
    print('-------------------------------') 
    
    # Realizando a inserção
    query = "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)"
    cursor.execute(query, (nome, preco, estoque))
    conn.commit()
    
    # Confirmação comm base na contagem de linhas / registros
    if cursor.rowcount > 0:
        print(f'\n>>> O produto: {nome} foi adicionado com sucesso! <<<')
    else:
        print(f'\n>>> Produto não cadastrado! <<<')
    cursor.close()
    desconectar(conn)        

# Funcionalidade atualizar produtos, com base no ID
def atualizar():
    print('---------- ATUALIZAR PRODUTOS -----------') 
    # Parâmetros de conexão
    conn = conectar()
    cursor = conn.cursor()
    
    # Entrada do usuário = "Id"
    id_user = int(input('Informe o ID: '))
    
    # Consulta de campos e listagem da tabela "produtos"
    query = 'SELECT nome, preco, estoque FROM produtos WHERE id=?'
    cursor.execute(query,(id_user,))
    produto = cursor.fetchone()
    
    # Conferência - se existir produtos cadastrados
    if produto:
        # Os dados podem ser atualizado ou permanecer com as informações anteriores
        pd_atual, pr_atual, es_atual = produto
        if input(f'Deseja atualizar o produto: {produto[0]}? >>> ') == 's':
            n_produto = input(f'Atualizar produto [{pd_atual}]: ') or pd_atual
            
            cv_preco = input(f'Atualizar preço [R${pr_atual}]: ')
            n_preco = float(cv_preco) if cv_preco else pr_atual
            
            cv_estoque =  input(f'Atualizar quantidade: [{es_atual}]: ')           
            n_estoque = int(cv_estoque) if cv_estoque else es_atual
            
            # Atualizando a tabela
            cursor.execute("UPDATE produtos SET nome=?, preco=?, estoque=? WHERE id=?",(n_produto, n_preco, n_estoque, id_user))                
            conn.commit()
            print('----------------------------------------')
            print('\n>>> Produto atualizado! <<<')
        else:
            print('\n>>> Ataualização cancelada! <<<')
    else:
        print('\n>>> Produto inexistente <<<')
    cursor.close()
    desconectar(conn)            
                                            
# Funcionalidade exclusão de produtos, com base no "Id"
def deletar():
    print('---------- EXCLUIR PRODUTO -----------') 
    # Parâmetros de conexão
    conn = conectar()
    cursor = conn.cursor()
    
    # Recebendo o "Id" do usuário
    id_user = int(input('Informe o ID: '))
    
    # Realzando consulta e listando os dados da tabela
    query = 'SELECT nome, preco, estoque FROM produtos WHERE id=?'
    cursor.execute(query,(id_user,))
    produto = cursor.fetchone()
    
    # Conferência -se houve produtos cadastrados
    if produto:
        if input(f'Deseja excluir o produto: {produto[0]}? >>> ') == 's':
            cursor.execute('DELETE FROM produtos WHERE id=?',(id_user,))
            print('----------------------------------------')
            print('\n >>> Produto excluído! <<<')
            conn.commit()
        else:
            print('\n >>> Exlusão cancelada! <<<')
    else:
        print('\n>>> Produto inexistente <<<')
    cursor.close()
    desconectar(conn)                    
    
# Funcionalidade Painel de opções - Menu
def menu():
    
    print('========= MENU DE OPÇÕES ==========')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    print('5 - Sair.')
    print('===================================')    
    # Realiza um loop enquanto validar a consulta
    while True:
        opcao = int(input('>>> Opção: '))
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        elif opcao == 5:
            print('\n>>> Consulta encerrada. <<<')
            break
        else:
            print('Opção inválida. Informe a opção correta')
            continue
        if input('\nNova solicitação (s - sim / n - não)?: ') != 's':
            print('\n>>> Consulta encerrada. <<<')
            break    
