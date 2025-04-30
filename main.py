#back end app#
import requests
from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervendas import BannerVenda
from functools import partial
import os
from myfirebase import MyFirebase
from bannervendedor import BannerVendedor
from datetime import date


GUI = Builder.load_file("main.kv")
class MainApp(App):
    cliente = None
    produto = None
    unidade = None
    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        #carregar as fotos dos clientes
        arquivos_clientes = os.listdir('icones/fotos_clientes')
        pagina_adicionarcliente = self.root.ids['adicionarvendaspage']
        lista_clientes = pagina_adicionarcliente.ids['lista_cliente']
        for foto in arquivos_clientes:
            imagem = ImageButton(source=f'icones/fotos_clientes/{foto}', on_release=partial(self.selecionar_cliente, foto))
            label = LabelButton(text=foto.replace(".png", "").capitalize(), on_release=partial(self.selecionar_cliente, foto))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)
        #carregar as fotos dos produtos
        arquivos_produtos = os.listdir('icones/fotos_produtos')
        pagina_adicionarvenda = self.root.ids['adicionarvendaspage']
        lista_produtos = pagina_adicionarvenda.ids['lista_produto']
        for foto in arquivos_produtos:
            imagem = ImageButton(source=f'icones/fotos_produtos/{foto}', on_release=partial(self.selecionar_produto, foto))
            label = LabelButton(text=foto.replace(".png", "").capitalize(), on_release=partial(self.selecionar_produto, foto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        #carregar a data
        pagina_adicionarvendas = self.root.ids['adicionarvendaspage']
        label_data = pagina_adicionarvendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"
        #carregar
        self.carregar_infos_user()
        self.mudar_tela('homepage')
    def carregar_infos_user(self):
        try:
            with open('refresh_token.txt', 'r') as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            #requisicao
            requisicao = requests.get(f'https://appvendashash-b902a-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}')
            requisicao_dict = requisicao.json()

            #avatar
            avatar = requisicao_dict['avatar']
            self.avatar = avatar
            foto_perfil = self.root.ids['foto_perfil']
            foto_perfil.source = f'icones/fotos_perfil/{avatar}'

            pagina_mudarfoto = self.root.ids['mudarfotoperfilpage']
            lista_fotos = pagina_mudarfoto.ids['lista_fotos']
            arquivos = os.listdir('icones/fotos_perfil')
            for foto in arquivos:
                imagem = ImageButton(source=f'icones/fotos_perfil/{foto}',
                                     on_release=partial(self.mudarfotoperfil, foto))
                lista_fotos.add_widget(imagem)

            #preencher total de vendas
            total_vendas = requisicao_dict['total_vendas']
            self.total_vendas = total_vendas
            homepage = self.root.ids['homepage']
            homepage.ids['label_total_vendas'].text = f'[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]'

            #preencher ID Unico
            id_vendedor = requisicao_dict['id_vendedor']
            self.id_vendedor = id_vendedor
            pagina_ajustes = self.root.ids['ajustespage']
            pagina_ajustes.ids['id_vendedor'].text = f'Seu ID Único: {id_vendedor}'

            # preencher lista de vendas
            pagina_homepage = self.root.ids['homepage']
            lista_vendas = pagina_homepage.ids['lista_vendas']

            # preencher equipe
            self.equipe = requisicao_dict['equipe']
            try:
                vendas = requisicao_dict['vendas']
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                                         produto=venda['produto'], foto_produto=venda['foto_produto'],
                                         data=venda['data'], unidade=venda['unidade'],
                                         preco=venda['preco'], quantidade=venda['quantidade'])
                    lista_vendas.add_widget(banner)
            except Exception as excecao:
                print(excecao)
        except:
            pass

        equipe = requisicao_dict["equipe"]
        lista_equipe = equipe.split(",")
        pagina_lista_vendedores = self.root.ids["listarvendedorespage"]
        lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]
        for id_vendedor_equipe in lista_equipe:
            id_vendedor_equipe = id_vendedor_equipe.strip().strip('"')  # Remove espaços e aspas
            if id_vendedor_equipe != "":
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                lista_vendedores.add_widget(banner_vendedor)
        self.mudar_tela('homepage')
    def mudar_tela(self, id_tela):
        #self.roots é o arquivo que eu carreguei com o builder
        gerenciador_de_telas = self.root.ids['screen_manager']
        #pega o gerenciador de telas pra falar de forma mais facil, pegando os ids do main e selecionando o screen
        gerenciador_de_telas.current = id_tela
    def mudarfotoperfil(self, foto, *args):
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f'icones/fotos_perfil/{foto}'
        info = f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(f'https://appvendashash-b902a-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}',
                                    data=str(info))

        self.mudar_tela("ajustespage")
    def adicionar_vendedor(self, id_vendedor_adicionado):
        link = f'https://appvendashash-b902a-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        pagina_adicionar_vendedor = self.root.ids["acompanharvendedorpage"]
        mensagem_texto = pagina_adicionar_vendedor.ids["mensagem_outrovendedor"]
        if requisicao_dic == {}:
            mensagem_texto.text = "Usuário não encontrado."
        else:
            equipe = self.equipe.split(",")
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = "Vendedor já faz parte da sua equipe."
            else:
                mensagem_texto.text = "Vendedor adicionado com sucesso!"
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"
                info = f'{{"equipe": "{self.equipe}"}}'
                requests.patch(f'https://appvendashash-b902a-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}',
                               data=info)
                pagina_lista_vendedores = self.root.ids["listarvendedorespage"]
                lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                lista_vendedores.add_widget(banner_vendedor)
    def selecionar_cliente(self, foto, *args):
        self.cliente = foto.replace(".png", "")
        pagina_adicionarcliente = self.root.ids['adicionarvendaspage']
        lista_clientes = pagina_adicionarcliente.ids['lista_cliente']
        for item in list(lista_clientes.children):
            item.color = (1, 1, 1, 1)
            try:
                texto = item.text.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207 / 255, 219 / 255, 1)
            except:
                pass
    def selecionar_produto(self, foto, *args):
        self.produto = foto.replace(".png", "")
        #selecionar pagina pra escolher os ids
        pagina_adicionarcliente = self.root.ids['adicionarvendaspage']
        #selecionando o scrollview
        lista_produto = pagina_adicionarcliente.ids['lista_produto']
        #pra pintar todos do scrollview de branco
        for item in list(lista_produto.children):
            item.color = (1,1,1,1)
            try:
                texto = item.text.lower() + ".png"
                #verificando se a foto é igual ao texto
                if foto == texto:
                    item.color = (0,207/255,219/255,1)
            except:
                pass
    def selecionar_unidades(self, id_label, *args):
        self.unidade = id_label
        #selecionar página pra escolher os ids
        pagina_adicionarcliente = self.root.ids['adicionarvendaspage']

        #pintando todos de branco
        pagina_adicionarcliente.ids["unidades_unidades"].color = (1,1,1,1)
        pagina_adicionarcliente.ids["unidades_kg"].color = (1,1,1,1)
        pagina_adicionarcliente.ids["unidades_litros"].color = (1,1,1,1)

        #on_release
        pagina_adicionarcliente.ids[id_label].color = (0,207/255,219/255,1)
    def adicionar_venda(self):
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade.replace("unidades_", "")
        pagina_adicionar_cliente = self.root.ids['adicionarvendaspage']
        data = pagina_adicionar_cliente.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_adicionar_cliente.ids['preco_total'].text
        quantidade = pagina_adicionar_cliente.ids['quantidade'].text

        if not cliente:
            pagina_adicionar_cliente.ids['selecionar_cliente'].color = (1, 0, 0, 1)
        if not produto:
            pagina_adicionar_cliente.ids['selecionar_produto'].color = (1, 0, 0, 1)
        if not unidade:
            pagina_adicionar_cliente.ids['unidades_unidades'].color = (1, 0, 0, 1)
            pagina_adicionar_cliente.ids['unidades_litros'].color = (1, 0, 0, 1)
            pagina_adicionar_cliente.ids['unidades_kg'].color = (1, 0, 0, 1)

        if not preco:
            pagina_adicionar_cliente.ids['label_preco'].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_adicionar_cliente.ids['label_preco'].color = (1, 0, 0, 1)
        if not quantidade:
            pagina_adicionar_cliente.ids['label_quantidade'].color = (1, 0, 0, 1)
        else:
            try:
                quantidade = float(quantidade)
            except:
                pagina_adicionar_cliente.ids['label_quantidade'].color = (1, 0, 0, 1)

        if cliente and produto and unidade and preco and quantidade and (type(quantidade) == float) and (type(preco) == float):
            foto_produto = produto + ".png"
            foto_cliente = cliente + ".png"

            info = f'{{"cliente": "{cliente}", "produto": "{produto}", "unidade": "{unidade}", "foto_produto": "{foto_produto}", "foto_cliente": "{foto_cliente}", "quantidade": "{quantidade}", "preco": "{preco}", "data": "{data}"}}'

            requests.post(f'https://appvendashash-b902a-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}', data=info)
        self.cliente = None
        self.produto = None
        self.unidade = None
        banner = BannerVenda(foto_cliente=foto_cliente, foto_produto=foto_produto, produto=produto,
                             cliente=cliente, preco=preco, unidade=unidade, quantidade=quantidade, data=data)
        pagina_homepage = self.root.ids["homepage"]
        lista_vendas = pagina_homepage.ids["lista_vendas"]
        lista_vendas.add_widget(banner)

        requisicao = requests.get(f'https://appvendashash-b902a-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}')
        total_vendas = float(requisicao.json())
        total_vendas += preco
        info = f'{{"total_vendas": "{total_vendas}"}}'
        requests.patch(f'https://appvendashash-b902a-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}', data=info)
        homepage = self.root.ids['homepage']
        homepage.ids['label_total_vendas'].text = f'[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]'
        self.mudar_tela("homepage")

    def carregar_todas_as_vendas(self):
        pagina_todasvendas = self.root.ids['vervendaspage']
        lista_vendas = pagina_todasvendas.ids["lista_vendas"]
        #verificar se ja existe banner
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)
        #preencher a página todas as vendas page
        #pegar as info da empresa
        requisicao = requests.get(f'https://appvendashash-b902a-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_dict = requisicao.json()
        print(requisicao_dict)

        # avatar empresa
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f'icones/fotos_perfil/hash.png'

        #preencher lista de vendas
        total_vendas = 0
        for local_id_usuario in requisicao_dict:
            try:
                vendas = requisicao_dict[local_id_usuario]["vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    total_vendas += float(venda["preco"])
                    banner = BannerVenda(cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                                         produto=venda['produto'], foto_produto=venda['foto_produto'],
                                         data=venda['data'], unidade=venda['unidade'],
                                         preco=venda['preco'], quantidade=venda['quantidade'])
                    lista_vendas.add_widget(banner)
            except Exception as excecao:
                pass
        # preencher total de vendas
        pagina_todasvendas.ids['label_total_vendas'].text = f'[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]'
        #ir pra pagina todas as vendas
        self.mudar_tela("vervendaspage")
    def sair_todasvendas(self, id_tela):

        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"
        self.mudar_tela(id_tela)

    def carregar_vendas_vendedor(self, dic_info_vendedor, *args):
        try:
            vendas = dic_info_vendedor["vendas"]
            paginaoutrovendedor = self.root.ids["vendasoutrovendedorpage"]
            lista_vendas = paginaoutrovendedor.ids["lista_vendas"]
            #verificar se ja existe banner
            for item in list(lista_vendas.children):
                lista_vendas.remove_widget(item)
            for id_venda in vendas:
                venda = vendas[id_venda]
                banner = BannerVenda(cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                                     produto=venda['produto'], foto_produto=venda['foto_produto'],
                                     data=venda['data'], unidade=venda['unidade'],
                                     preco=venda['preco'], quantidade=venda['quantidade'])
                lista_vendas.add_widget(banner)
        except Exception as excecao:
            print(excecao)

        #preencher total vendas
        total_vendas = dic_info_vendedor['total_vendas']
        paginaoutrovendedor.ids['label_total_vendas'].text = f'[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]'

        #preencher avatar
        foto_perfil = self.root.ids['foto_perfil']
        avatar = dic_info_vendedor['avatar']
        foto_perfil.source = f'icones/fotos_perfil/{avatar}'

        self.mudar_tela("vendasoutrovendedorpage")

MainApp().run()