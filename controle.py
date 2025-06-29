from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0
numero_id_1 = 0
usuario = ""

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

def chama_login():
    global usuario
    login.label_4.setText("")
    nome_usuario = login.lineEdit.text()
    senha = login.lineEdit_2.text()
    if nome_usuario == "Master" and senha == "1110" :
        login.close()
        usuario = nome_usuario
        principal.show()
    elif nome_usuario == "Padrao" and senha == "1210" :
        login.close()
        principal.show()
    else:
        login.label_4.setText("Dados de login incorretos")

def chama_logout():
    global usuario

    principal.close()
    login.show()
    usuario = ""

    # Limpa os campos
    login.lineEdit.setText("")
    login.lineEdit_2.setText("")

def selecao_produto():

    if not (principal.radioButton.isChecked() or 
            principal.radioButton_2.isChecked() or 
            principal.radioButton_3.isChecked()):
        QMessageBox.warning(principal, "Atenção", "Selecione uma categoria antes de continuar.")
        return  # Sai da função sem fazer nada

    if principal.radioButton.isChecked():
        categoria = "Bolos"

        if categoria == "Bolos" and usuario == 'Master':
            cad_bolos.show()

        else:
            categoria == "Bolos" and usuario == 'Padrao'
            consultar_bolos_1()

    if principal.radioButton_2.isChecked():
        categoria = "Docinhos"

        if categoria == "Docinhos" and usuario == 'Master':
            cad_docinhos.show()

        else:
            categoria == "Docinhos" and usuario == 'uPadraoser'
            consultar_docinhos_1()

    if principal.radioButton_3.isChecked():
        categoria = "Chocolates"

        if categoria == "Chocolates" and usuario == 'Master':
            cad_chocolates.show()

        else:
            categoria == "Chocolates" and usuario == 'Padrao'
            consultar_chocolates_1()


def cadastrar_bolos():
    global categoria
    linha1 = cad_bolos.lineEdit.text()
    linha2 = cad_bolos.lineEdit_2.text()
    linha3 = cad_bolos.lineEdit_3.text()
    linha4 = cad_bolos.lineEdit_4.text()
    linha5 = cad_bolos.lineEdit_5.text()
    linha6 = cad_bolos.lineEdit_6.text()
    categoria = ""

    # Verifica campos obrigatórios
    if not linha1 or not linha2 or not linha3 or not linha4 or not linha5 or not linha6:
        QMessageBox.warning(cad_bolos, "Erro", "Todos os campos devem ser preenchidos.")
        return
    
# Verifica se o ID já existe
    try:
        cursor = banco.cursor()
        cursor.execute("SELECT COUNT(*) FROM bolos WHERE id = %s", (linha1,))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            QMessageBox.warning(cad_bolos, "ID Duplicado", "Já existe um produto cadastrado com este Código.")
            return
    except Exception as e:
        QMessageBox.critical(cad_bolos, "Erro", f"Erro ao verificar ID no banco:\n{str(e)}")
        return
    
    # Verifica se linha1 é um número inteiro
    try:
        linha1 = int(linha1)
    except ValueError:
        QMessageBox.critical(cad_bolos, "Erro", "O Código deve ser um número válido..")
        return
    
        # Verifica se linha2 é um número inteiro
    try:
        linha2 = int(linha2)
    except ValueError:
        QMessageBox.critical(cad_bolos, "Erro", "A Quantidade deve ser um número válido.")
        return
    
    # Verifica e converte o preço
    try:
        linha5 = float(linha5.replace(",", "."))  # aceita vírgula como separador decimal
    except ValueError:
        QMessageBox.critical(cad_bolos, "Erro", "O preço deve ser um número válido.")
        return
    
    try:
        linha6 = float(linha6.replace(",", "."))  # aceita vírgula como separador decimal
    except ValueError:
        QMessageBox.critical(cad_bolos, "Erro", "O peso deve ser um número válido.")
        return

    try:
        cursor = banco.cursor()
        comando_SQL = """
            INSERT INTO bolos (id, quantidade, nome, descricao, preco, peso)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        dados = (linha1, linha2, linha3, linha4, linha5, linha6)
        cursor.execute(comando_SQL, dados)
        banco.commit()

        # Limpa os campos
        cad_bolos.lineEdit.setText("")
        cad_bolos.lineEdit_2.setText("")
        cad_bolos.lineEdit_3.setText("")
        cad_bolos.lineEdit_4.setText("")
        cad_bolos.lineEdit_5.setText("")
        cad_bolos.lineEdit_6.setText("")

        # Mensagem de sucesso
        QMessageBox.information(cad_bolos, "Sucesso", "Produto cadastrado com sucesso!")

    except Exception as e:
        QMessageBox.critical(cad_bolos, "Erro", f"Ocorreu um erro ao inserir no banco:\n{str(e)}")

def editar_bolos():
    global numero_id
    linha = list_bolos.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM bolos")
    dados_lidos = cursor.fetchall()

    # Verifica se há dados no banco
    if not dados_lidos:
        QMessageBox.information(list_bolos, "Aviso", "Não há produtos cadastrados para editar.")
        return

    # Verifica se alguma linha foi selecionada
    if linha < 0 or linha >= len(dados_lidos):
        QMessageBox.warning(list_bolos, "Atenção", "Selecione um produto para editar.")
        return

    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM bolos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()

    mod_bolos.show()
    numero_id = valor_id

    mod_bolos.lineEdit.setText(str(produto[0][0]))
    mod_bolos.lineEdit_2.setText(str(produto[0][1]))
    mod_bolos.lineEdit_3.setText(str(produto[0][2]))
    mod_bolos.lineEdit_4.setText(str(produto[0][3]))
    mod_bolos.lineEdit_5.setText(str(produto[0][4]))
    mod_bolos.lineEdit_6.setText(str(produto[0][5]))

 

def salvar_bolos():
    global numero_id

    # Pega os valores dos campos da interfaceS
    
    id = mod_bolos.lineEdit.text()
    quantidade = mod_bolos.lineEdit_2.text()
    nome = mod_bolos.lineEdit_3.text()
    descricao = mod_bolos.lineEdit_4.text()
    preco = mod_bolos.lineEdit_5.text()
    peso = mod_bolos.lineEdit_6.text()

    print(quantidade + descricao)

    # Verifica se o novo ID já existe em outro produto
    try:
        cursor = banco.cursor()
        cursor.execute("SELECT id FROM bolos WHERE id = %s AND id != %s", (id, numero_id))
        resultado = cursor.fetchone()
        if resultado:
            QMessageBox.warning(mod_bolos, "ID Duplicado", "Já existe outro produto com este ID.")
            return
    except Exception as e:
        QMessageBox.critical(mod_bolos, "Erro", f"Erro ao verificar ID no banco:\n{str(e)}")
        return

    # Atualiza os dados no banco de forma segura
    cursor = banco.cursor()
    sql = """
        UPDATE bolos
        SET id = %s, quantidade = %s, nome = %s, descricao = %s, preco = %s, peso = %s
        WHERE id = %s
    """
    valores = (id, quantidade, nome, descricao, preco, peso, numero_id)
    cursor.execute(sql, valores)

    banco.commit()  # Garante que as alterações sejam salvas

    #atualizar as janelas
    mod_bolos.close()
    consultar_bolos()

def excluir_bolos():
    linha = list_bolos.tableWidget.currentRow()

    if linha == -1:
        QMessageBox.warning(list_bolos, "Aviso", "Selecione um item para excluir.")
        return

    resposta = QMessageBox.question(
        list_bolos,
        "Confirmar Exclusão",
        "Tem certeza que deseja excluir este produto?",
        QMessageBox.Yes | QMessageBox.No
    )

    if resposta == QMessageBox.No:
        return

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM bolos")
    dados_lidos = cursor.fetchall()

    try:
        valor_id = dados_lidos[linha][0]
        cursor.execute("DELETE FROM bolos WHERE id = %s", (valor_id,))
        banco.commit()

        list_bolos.tableWidget.removeRow(linha)
        QMessageBox.information(list_bolos, "Sucesso", "Produto excluído com sucesso!")

    except IndexError:
        QMessageBox.critical(list_bolos, "Erro", "Falha ao excluir: índice inválido.")
    except Exception as e:
        QMessageBox.critical(list_bolos, "Erro", f"Erro ao excluir o produto:\n{str(e)}")
    

def pdf_bolos():
    print("gerar pdf bolos")
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM bolos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_bolos.pdf")
    pdf.setFont("Times-Bold", 12)
    pdf.drawString(250,800, "bolos cadastrados")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(20,750, "CÓDIGO")
    pdf.drawString(70,750, "QTD.")
    pdf.drawString(110,750, "NOME")
    pdf.drawString(240,750, "DESCRICAO")
    pdf.drawString(450,750, "PREÇO (R$)")
    pdf.drawString(530,750, "PESO (kg)")

    for i in range(0,len(dados_lidos)):
        y = y + 25
        pdf.drawString(20,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(70,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(240,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(450,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(530,750 - y, str(dados_lidos[i][5]))
   
   
    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")

    # Mensagem de sucesso
    QMessageBox.information(list_bolos, "Sucesso", "PDF Gerado Com Sucesso!")

def consultar_bolos():
    list_bolos.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM bolos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    if not dados_lidos:
        QMessageBox.information(list_bolos, "Aviso", "Nenhum produto cadastrado.")
        list_bolos.tableWidget.setRowCount(0)
        return

    list_bolos.tableWidget.setRowCount(len(dados_lidos))
    list_bolos.tableWidget.setColumnCount(6)

    for i in range(len(dados_lidos)):
        for j in range(6):
            if j == 4:  # Coluna do preço
                valor_formatado = "{:.2f}".format(dados_lidos[i][j])
                list_bolos.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(valor_formatado))
            else:
                list_bolos.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    cad_bolos.close()

def consultar_bolos_1():
    list_bolos_1.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM bolos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    if not dados_lidos:
        QMessageBox.information(list_bolos_1, "Aviso", "Nenhum produto cadastrado.")
        list_bolos.tableWidget.setRowCount(0)
        return

    list_bolos_1.tableWidget.setRowCount(len(dados_lidos))
    list_bolos_1.tableWidget.setColumnCount(6)

    for i in range(len(dados_lidos)):
        for j in range(6):
            if j == 4:  # Coluna do preço
                valor_formatado = "{:.2f}".format(dados_lidos[i][j])
                list_bolos_1.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(valor_formatado))
            else:
                list_bolos_1.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def cadastrar_docinhos():
    global categoria
    linha1 = cad_docinhos.lineEdit.text()
    linha2 = cad_docinhos.lineEdit_2.text()
    linha3 = cad_docinhos.lineEdit_3.text()
    linha4 = cad_docinhos.lineEdit_4.text()
    linha5 = cad_docinhos.lineEdit_5.text()
    linha6 = cad_docinhos.lineEdit_6.text()
    categoria = ""

    # Verifica campos obrigatórios
    if not linha1 or not linha2 or not linha3 or not linha4 or not linha5 or not linha6:
        QMessageBox.warning(cad_docinhos, "Erro", "Todos os campos devem ser preenchidos.")
        return
    
    # Verifica se o ID já existe
    try:
        cursor = banco.cursor()
        cursor.execute("SELECT COUNT(*) FROM docinhos WHERE id = %s", (linha1,))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            QMessageBox.warning(cad_docinhos, "ID Duplicado", "Já existe um produto cadastrado com este Código.")
            return
    except Exception as e:
        QMessageBox.critical(cad_docinhos, "Erro", f"Erro ao verificar ID no banco:\n{str(e)}")
        return
    
        # Verifica se linha1 é um número inteiro
    try:
        linha1 = int(linha1)
    except ValueError:
        QMessageBox.critical(cad_docinhos, "Erro", "O Código deve ser um número válido.")
        return
    
        # Verifica se linha2 é um número inteiro
    try:
        linha2 = int(linha2)
    except ValueError:
        QMessageBox.critical(cad_docinhos, "Erro", "A Quantidade deve ser um número válido.")
        return

    # Verifica e converte o preço
    try:
        linha5 = float(linha5.replace(",", "."))  # aceita vírgula como separador decimal
    except ValueError:
        QMessageBox.critical(cad_docinhos, "Erro", "O preço deve ser um número válido.")
        return
    
    try:
        linha6 = float(linha6.replace(",", "."))  # aceita vírgula como separador decimal
    except ValueError:
        QMessageBox.critical(cad_docinhos, "Erro", "O peso deve ser um número válido.")
        return

    try:
        cursor = banco.cursor()
        comando_SQL = """
            INSERT INTO docinhos (id, quantidade, nome, descricao, preco, unidade)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        dados = (linha1, linha2, linha3, linha4, linha5, linha6)
        cursor.execute(comando_SQL, dados)
        banco.commit()

        # Limpa os campos
        cad_docinhos.lineEdit.setText("")
        cad_docinhos.lineEdit_2.setText("")
        cad_docinhos.lineEdit_3.setText("")
        cad_docinhos.lineEdit_4.setText("")
        cad_docinhos.lineEdit_5.setText("")
        cad_docinhos.lineEdit_6.setText("")

        # Mensagem de sucesso
        QMessageBox.information(cad_docinhos, "Sucesso", "Produto cadastrado com sucesso!")

    except Exception as e:
        QMessageBox.critical(cad_docinhos, "Erro", f"Ocorreu um erro ao inserir no banco:\n{str(e)}")

def editar_docinhos():
    global numero_id
    linha = list_docinhos.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM docinhos")
    dados_lidos = cursor.fetchall()

    # Verifica se há dados no banco
    if not dados_lidos:
        QMessageBox.information(list_docinhos, "Aviso", "Não há produtos cadastrados para editar.")
        return

    # Verifica se alguma linha foi selecionada
    if linha < 0 or linha >= len(dados_lidos):
        QMessageBox.warning(list_docinhos, "Atenção", "Selecione um produto para editar.")
        return

    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM docinhos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()

    mod_docinhos.show()
    numero_id = valor_id

    mod_docinhos.lineEdit.setText(str(produto[0][0]))
    mod_docinhos.lineEdit_2.setText(str(produto[0][1]))
    mod_docinhos.lineEdit_3.setText(str(produto[0][2]))
    mod_docinhos.lineEdit_4.setText(str(produto[0][3]))
    mod_docinhos.lineEdit_5.setText(str(produto[0][4]))
    mod_docinhos.lineEdit_6.setText(str(produto[0][5]))

def salvar_docinhos():
    global numero_id

    # Pega os valores dos campos da interfaceS
    
    id = mod_docinhos.lineEdit.text()
    quantidade = mod_docinhos.lineEdit_2.text()
    nome = mod_docinhos.lineEdit_3.text()
    descricao = mod_docinhos.lineEdit_4.text()
    preco = mod_docinhos.lineEdit_5.text()
    unidade = mod_docinhos.lineEdit_6.text()

    print(quantidade + descricao)

    # Verifica se o novo ID já existe em outro produto
    try:
        cursor = banco.cursor()
        cursor.execute("SELECT id FROM docinhos WHERE id = %s AND id != %s", (id, numero_id))
        resultado = cursor.fetchone()
        if resultado:
            QMessageBox.warning(mod_docinhos, "ID Duplicado", "Já existe outro produto com este ID.")
            return
    except Exception as e:
        QMessageBox.critical(mod_docinhos, "Erro", f"Erro ao verificar ID no banco:\n{str(e)}")
        return

    # Atualiza os dados no banco de forma segura
    cursor = banco.cursor()
    sql = """
        UPDATE docinhos
        SET id = %s, quantidade = %s, nome = %s, descricao = %s, preco = %s, unidade = %s
        WHERE id = %s
    """
    valores = (id, quantidade, nome, descricao, preco, unidade, numero_id)
    cursor.execute(sql, valores)

    banco.commit()  # Garante que as alterações sejam salvas

    #atualizar as janelas
    mod_docinhos.close()
    consultar_docinhos()

def excluir_docinhos():
    linha = list_docinhos.tableWidget.currentRow()

    if linha == -1:
        QMessageBox.warning(list_docinhos, "Aviso", "Selecione um item para excluir.")
        return

    resposta = QMessageBox.question(
        list_docinhos,
        "Confirmar Exclusão",
        "Tem certeza que deseja excluir este produto?",
        QMessageBox.Yes | QMessageBox.No
    )

    if resposta == QMessageBox.No:
        return

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM docinhos")
    dados_lidos = cursor.fetchall()

    try:
        valor_id = dados_lidos[linha][0]
        cursor.execute("DELETE FROM docinhos WHERE id = %s", (valor_id,))
        banco.commit()

        list_docinhos.tableWidget.removeRow(linha)
        QMessageBox.information(list_docinhos, "Sucesso", "Produto excluído com sucesso!")

    except IndexError:
        QMessageBox.critical(list_docinhos, "Erro", "Falha ao excluir: índice inválido.")
    except Exception as e:
        QMessageBox.critical(list_docinhos, "Erro", f"Erro ao excluir o produto:\n{str(e)}")
    

def pdf_docinhos():
    print("gerar pdf docinhos")
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM docinhos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_docinhos.pdf")
    pdf.setFont("Times-Bold", 12)
    pdf.drawString(250,800, "docinhos cadastrados")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(20,750, "CÓDIGO")
    pdf.drawString(70,750, "QTD.")
    pdf.drawString(110,750, "NOME")
    pdf.drawString(240,750, "DESCRICAO")
    pdf.drawString(450,750, "PREÇO (R$)")
    pdf.drawString(530,750, "UNIDADE (Un.)")

    for i in range(0,len(dados_lidos)):
        y = y + 25
        pdf.drawString(20,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(70,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(240,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(450,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(530,750 - y, str(dados_lidos[i][5]))
   
   
    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")

    # Mensagem de sucesso
    QMessageBox.information(list_docinhos, "Sucesso", "PDF Gerado Com Sucesso!")

def consultar_docinhos():
    list_docinhos.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM docinhos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    if not dados_lidos:
        QMessageBox.information(list_docinhos, "Aviso", "Nenhum produto cadastrado.")
        list_docinhos.tableWidget.setRowCount(0)
        return

    list_docinhos.tableWidget.setRowCount(len(dados_lidos))
    list_docinhos.tableWidget.setColumnCount(6)

    for i in range(len(dados_lidos)):
        for j in range(6):
            if j == 4:  # Coluna do preço
                valor_formatado = "{:.2f}".format(dados_lidos[i][j])
                list_docinhos.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(valor_formatado))
            else:
                list_docinhos.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def consultar_docinhos_1():
    list_docinhos_1.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM docinhos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    if not dados_lidos:
        QMessageBox.information(list_docinhos_1, "Aviso", "Nenhum produto cadastrado.")
        list_docinhos.tableWidget.setRowCount(0)
        return

    list_docinhos_1.tableWidget.setRowCount(len(dados_lidos))
    list_docinhos_1.tableWidget.setColumnCount(6)

    for i in range(len(dados_lidos)):
        for j in range(6):
            if j == 4:  # Coluna do preço
                valor_formatado = "{:.2f}".format(dados_lidos[i][j])
                list_docinhos_1.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(valor_formatado))
            else:
                list_docinhos_1.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def cadastrar_chocolates():
    global categoria
    linha1 = cad_chocolates.lineEdit.text()
    linha2 = cad_chocolates.lineEdit_2.text()
    linha3 = cad_chocolates.lineEdit_3.text()
    linha4 = cad_chocolates.lineEdit_4.text()
    linha5 = cad_chocolates.lineEdit_5.text()
    linha6 = cad_chocolates.lineEdit_6.text()
    categoria = ""

    # Verifica campos obrigatórios
    if not linha1 or not linha2 or not linha3 or not linha4 or not linha5 or not linha6:
        QMessageBox.warning(cad_chocolates, "Erro", "Todos os campos devem ser preenchidos.")
        return
    
   # Verifica se o ID já existe
    try:
        cursor = banco.cursor()
        cursor.execute("SELECT COUNT(*) FROM chocolates WHERE id = %s", (linha1,))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            QMessageBox.warning(cad_chocolates, "ID Duplicado", "Já existe um produto cadastrado com este Código.")
            return
    except Exception as e:
        QMessageBox.critical(cad_chocolates, "Erro", f"Erro ao verificar ID no banco:\n{str(e)}")
        return
    
            # Verifica se linha1 é um número inteiro
    try:
        linha1 = int(linha1)
    except ValueError:
        QMessageBox.critical(cad_chocolates, "Erro", "O Código deve ser um número válido.")
        return
    
        # Verifica se linha2 é um número inteiro
    try:
        linha2 = int(linha2)
    except ValueError:
        QMessageBox.critical(cad_chocolates, "Erro", "A Quantidade deve ser um número válido.")
        return

    # Verifica e converte o preço
    try:
        linha5 = float(linha5.replace(",", "."))  # aceita vírgula como separador decimal
    except ValueError:
        QMessageBox.critical(cad_chocolates, "Erro", "O preço deve ser um número válido.")
        return
    
    try:
        linha6 = float(linha6.replace(",", "."))  # aceita vírgula como separador decimal
    except ValueError:
        QMessageBox.critical(cad_chocolates, "Erro", "O peso deve ser um número válido.")
        return

    try:
        cursor = banco.cursor()
        comando_SQL = """
            INSERT INTO chocolates (id, quantidade, nome, descricao, preco, unidade)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        dados = (linha1, linha2, linha3, linha4, linha5, linha6)
        cursor.execute(comando_SQL, dados)
        banco.commit()

        # Limpa os campos
        cad_chocolates.lineEdit.setText("")
        cad_chocolates.lineEdit_2.setText("")
        cad_chocolates.lineEdit_3.setText("")
        cad_chocolates.lineEdit_4.setText("")
        cad_chocolates.lineEdit_5.setText("")
        cad_chocolates.lineEdit_6.setText("")

        # Mensagem de sucesso
        QMessageBox.information(cad_chocolates, "Sucesso", "Produto cadastrado com sucesso!")

    except Exception as e:
        QMessageBox.critical(cad_chocolates, "Erro", f"Ocorreu um erro ao inserir no banco:\n{str(e)}")

def editar_chocolates():
    global numero_id
    linha = list_chocolates.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM chocolates")
    dados_lidos = cursor.fetchall()

    # Verifica se há dados no banco
    if not dados_lidos:
        QMessageBox.information(list_chocolates, "Aviso", "Não há produtos cadastrados para editar.")
        return

    # Verifica se alguma linha foi selecionada
    if linha < 0 or linha >= len(dados_lidos):
        QMessageBox.warning(list_chocolates, "Atenção", "Selecione um produto para editar.")
        return

    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM chocolates WHERE id=" + str(valor_id))
    produto = cursor.fetchall()

    mod_chocolates.show()
    numero_id = valor_id

    mod_chocolates.lineEdit.setText(str(produto[0][0]))
    mod_chocolates.lineEdit_2.setText(str(produto[0][1]))
    mod_chocolates.lineEdit_3.setText(str(produto[0][2]))
    mod_chocolates.lineEdit_4.setText(str(produto[0][3]))
    mod_chocolates.lineEdit_5.setText(str(produto[0][4]))
    mod_chocolates.lineEdit_6.setText(str(produto[0][5]))

def salvar_chocolates():
    global numero_id

    # Pega os valores dos campos da interfaceS
    
    id = mod_chocolates.lineEdit.text()
    quantidade = mod_chocolates.lineEdit_2.text()
    nome = mod_chocolates.lineEdit_3.text()
    descricao = mod_chocolates.lineEdit_4.text()
    preco = mod_chocolates.lineEdit_5.text()
    unidade = mod_chocolates.lineEdit_6.text()

    print(quantidade + descricao)

    # Verifica se o novo ID já existe em outro produto
    try:
        cursor = banco.cursor()
        cursor.execute("SELECT id FROM chocolates WHERE id = %s AND id != %s", (id, numero_id))
        resultado = cursor.fetchone()
        if resultado:
            QMessageBox.warning(mod_chocolates, "ID Duplicado", "Já existe outro produto com este ID.")
            return
    except Exception as e:
        QMessageBox.critical(mod_chocolates, "Erro", f"Erro ao verificar ID no banco:\n{str(e)}")
        return

    # Atualiza os dados no banco de forma segura
    cursor = banco.cursor()
    sql = """
        UPDATE chocolates
        SET id = %s, quantidade = %s, nome = %s, descricao = %s, preco = %s, unidade = %s
        WHERE id = %s
    """
    valores = (id, quantidade, nome, descricao, preco, unidade, numero_id)
    cursor.execute(sql, valores)

    banco.commit()  # Garante que as alterações sejam salvas

    #atualizar as janelas
    mod_chocolates.close()
    consultar_chocolates()

def excluir_chocolates():
    linha = list_chocolates.tableWidget.currentRow()

    if linha == -1:
        QMessageBox.warning(list_chocolates, "Aviso", "Selecione um item para excluir.")
        return

    resposta = QMessageBox.question(
        list_chocolates,
        "Confirmar Exclusão",
        "Tem certeza que deseja excluir este produto?",
        QMessageBox.Yes | QMessageBox.No
    )

    if resposta == QMessageBox.No:
        return

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM chocolates")
    dados_lidos = cursor.fetchall()

    try:
        valor_id = dados_lidos[linha][0]
        cursor.execute("DELETE FROM chocolates WHERE id = %s", (valor_id,))
        banco.commit()

        list_chocolates.tableWidget.removeRow(linha)
        QMessageBox.information(list_chocolates, "Sucesso", "Produto excluído com sucesso!")

    except IndexError:
        QMessageBox.critical(list_chocolates, "Erro", "Falha ao excluir: índice inválido.")
    except Exception as e:
        QMessageBox.critical(list_chocolates, "Erro", f"Erro ao excluir o produto:\n{str(e)}")
    

def pdf_chocolates():
    print("gerar pdf chocolates")
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM chocolates"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_chocolates.pdf")
    pdf.setFont("Times-Bold", 12)
    pdf.drawString(250,800, "chocolates cadastrados")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(20,750, "CÓDIGO")
    pdf.drawString(70,750, "QTD.")
    pdf.drawString(110,750, "NOME")
    pdf.drawString(240,750, "DESCRICAO")
    pdf.drawString(450,750, "PREÇO (R$)")
    pdf.drawString(530,750, "UNIDADE (Un.)")

    for i in range(0,len(dados_lidos)):
        y = y + 25
        pdf.drawString(20,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(70,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(240,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(450,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(530,750 - y, str(dados_lidos[i][5]))
   
   
    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")

    # Mensagem de sucesso
    QMessageBox.information(list_chocolates, "Sucesso", "PDF Gerado Com Sucesso!")

def consultar_chocolates():
    list_chocolates.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM chocolates"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    if not dados_lidos:
        QMessageBox.information(list_chocolates, "Aviso", "Nenhum produto cadastrado.")
        list_chocolates.tableWidget.setRowCount(0)
        return

    list_chocolates.tableWidget.setRowCount(len(dados_lidos))
    list_chocolates.tableWidget.setColumnCount(6)

    for i in range(len(dados_lidos)):
        for j in range(6):
            if j == 4:  # Coluna do preço
                valor_formatado = "{:.2f}".format(dados_lidos[i][j])
                list_chocolates.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(valor_formatado))
            else:
                list_chocolates.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def consultar_chocolates_1():
    list_chocolates_1.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM chocolates"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    if not dados_lidos:
        QMessageBox.information(list_chocolates_1, "Aviso", "Nenhum produto cadastrado.")
        list_chocolates_1.tableWidget.setRowCount(0)
        return

    list_chocolates_1.tableWidget.setRowCount(len(dados_lidos))
    list_chocolates_1.tableWidget.setColumnCount(6)

    for i in range(len(dados_lidos)):
        for j in range(6):
            if j == 4:  # Coluna do preço
                valor_formatado = "{:.2f}".format(dados_lidos[i][j])
                list_chocolates_1.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(valor_formatado))
            else:
                list_chocolates_1.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app=QtWidgets.QApplication([])
login=uic.loadUi("login.ui")
login.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
login.setFixedSize(login.size())

principal=uic.loadUi("principal.ui")
principal.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
principal.setFixedSize(principal.size())


login.pushButton.clicked.connect(chama_login)
login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
principal.pushButton_3.clicked.connect(chama_logout)
principal.pushButton_2.clicked.connect(selecao_produto)

cad_bolos=uic.loadUi("cad_bolos.ui")
cad_bolos.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
cad_bolos.setFixedSize(principal.size())

list_bolos=uic.loadUi("list_bolos.ui")
list_bolos.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
list_bolos.setFixedSize(principal.size())

list_bolos_1=uic.loadUi("list_bolos_1.ui")
list_bolos_1.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
list_bolos_1.setFixedSize(principal.size())

mod_bolos=uic.loadUi("mod_bolos.ui")
mod_bolos.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
mod_bolos.setFixedSize(mod_bolos.size())

cad_bolos.pushButton.clicked.connect(cadastrar_bolos)
cad_bolos.pushButton_2.clicked.connect(consultar_bolos)
list_bolos.pushButton_3.clicked.connect(editar_bolos)
list_bolos.pushButton_2.clicked.connect(excluir_bolos)
list_bolos.pushButton.clicked.connect(pdf_bolos)
list_bolos_1.pushButton.clicked.connect(pdf_bolos)
mod_bolos.pushButton.clicked.connect(salvar_bolos)

cad_docinhos=uic.loadUi("cad_docinhos.ui")
cad_docinhos.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
cad_docinhos.setFixedSize(principal.size())

list_docinhos=uic.loadUi("list_docinhos.ui")
list_docinhos.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
list_docinhos.setFixedSize(principal.size())

list_docinhos_1=uic.loadUi("list_docinhos_1.ui")
list_docinhos_1.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
list_docinhos_1.setFixedSize(principal.size())

mod_docinhos=uic.loadUi("mod_docinhos.ui")
mod_docinhos.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
mod_docinhos.setFixedSize(mod_docinhos.size())

cad_docinhos.pushButton.clicked.connect(cadastrar_docinhos)
cad_docinhos.pushButton_2.clicked.connect(consultar_docinhos)
list_docinhos.pushButton_3.clicked.connect(editar_docinhos)
list_docinhos.pushButton_2.clicked.connect(excluir_docinhos)
list_docinhos.pushButton.clicked.connect(pdf_docinhos)
list_docinhos_1.pushButton.clicked.connect(pdf_docinhos)
mod_docinhos.pushButton.clicked.connect(salvar_docinhos)

cad_chocolates=uic.loadUi("cad_chocolates.ui")
cad_chocolates.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
cad_chocolates.setFixedSize(principal.size())

list_chocolates=uic.loadUi("list_chocolates.ui")
list_chocolates.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
list_chocolates.setFixedSize(principal.size())

list_chocolates_1=uic.loadUi("list_chocolates_1.ui")
list_chocolates_1.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
list_chocolates_1.setFixedSize(principal.size())

mod_chocolates=uic.loadUi("mod_chocolates.ui")
mod_chocolates.setWindowFlags(QtCore.Qt.Window |
                         QtCore.Qt.WindowMinimizeButtonHint |
                         QtCore.Qt.WindowCloseButtonHint)
mod_chocolates.setFixedSize(mod_chocolates.size())

cad_chocolates.pushButton.clicked.connect(cadastrar_chocolates)
cad_chocolates.pushButton_2.clicked.connect(consultar_chocolates)
list_chocolates.pushButton_3.clicked.connect(editar_chocolates)
list_chocolates.pushButton_2.clicked.connect(excluir_chocolates)
list_chocolates.pushButton.clicked.connect(pdf_chocolates)
list_chocolates_1.pushButton.clicked.connect(pdf_chocolates)
mod_chocolates.pushButton.clicked.connect(salvar_chocolates)

login.show()
#formulario.show()
app.exec()

# use cadastro_produtos;

# create table bolos (
#     id INT NOT NULL AUTO_INCREMENT,
#     codigo INT,
#     nome  VARCHAR(50),
#     descricao VARCHAR(50),
#     preco DOUBLE,
#     peso DOUBLE,
#     PRIMARY KEY (id)
# );

# use cadastro_produtos;

# create table bolos (
#     id INT,
#     quantidade INT,
#     nome  VARCHAR(50),
#     descricao VARCHAR(50),
#     preco DOUBLE,
#     peso DOUBLE,
#     PRIMARY KEY (id)
# );

# use cadastro_produtos;

# create table docinhos (
#     id INT,
#     quantidade INT,
#     nome  VARCHAR(50),
#     descricao VARCHAR(50),
#     preco DOUBLE,
#     unidade DOUBLE,
#     PRIMARY KEY (id)
# );

# use cadastro_produtos;

# create table chocolates (
#     id INT,
#     quantidade INT,
#     nome  VARCHAR(50),
#     descricao VARCHAR(50),
#     preco DOUBLE,
#     unidade DOUBLE,
#     PRIMARY KEY (id)
# );
