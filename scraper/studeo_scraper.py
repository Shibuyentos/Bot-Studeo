# scraper/studeo_scraper.py

from selenium.webdriver.edge.service import Service 
from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class StudeoScraper:
    def __init__(self, driver_path: str):
        edge_options = Options()
        service = Service(executable_path=driver_path)
        self.driver = EdgeDriver(service=service, options=edge_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        print("Scraper para Microsoft Edge inicializado com driver manual.")

    def login(self, cpf, senha):
        try:
            url_login = 'https://studeo.unicesumar.edu.br/'
            print(f"Acessando {url_login}...")
            self.driver.get(url_login)

            print("Preenchendo credenciais...")
            campo_cpf = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            campo_cpf.send_keys(cpf)

            campo_senha = self.driver.find_element(By.ID, "password")
            campo_senha.send_keys(senha)

            botao_entrar = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            botao_entrar.click()
            print("Primeira etapa do login concluída.")
            
            try:
                print("Verificando a presença do banner de cookies...")
                seletor_cookie = "//button[contains(text(), 'Aceitar')]"
                botao_aceitar_cookie = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, seletor_cookie)))
                print("Banner de cookies encontrado. Clicando em 'Aceitar'...")
                botao_aceitar_cookie.click()
                time.sleep(1) 
            except TimeoutException:
                print("Banner de cookies não encontrado. Seguindo em frente.")

            print("Aguardando o botão 'Acessar' da modalidade...")
            seletor_botao_acessar = "button.btn-info[title='Acessar']"
            
            botoes_acessar = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor_botao_acessar)))
            
            print("Clicando no botão 'Acessar' (EAD) via JavaScript...")
            self.driver.execute_script("arguments[0].click();", botoes_acessar[0])
            
            print("Seleção de modalidade concluída!")
            
            try:
                print("Verificando pop-up de pesquisa NPS...")
                seletor_ignorar_aviso = "//button[contains(text(), 'Ignorar aviso')]"
                botao_ignorar = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, seletor_ignorar_aviso)))
                print("Pop-up NPS encontrado. Clicando para ignorar...")
                botao_ignorar.click()
            except TimeoutException:
                print("Pop-up NPS não encontrado.")

            print("Login 100% concluído! Acesso à página principal liberado.")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Ocorreu um erro durante o login: {e}")
            return False

    def checar_atividades_pendentes(self):
        print("\nIniciando verificação de atividades pendentes...")
        atividades = []
        try:
            print("Procurando o botão 'Atividades' com o seletor XPath...")
            seletor_atividades_xpath = "//a[.//span[text()='Atividades']]"
            
            botao_atividades = self.wait.until(EC.presence_of_element_located((By.XPATH, seletor_atividades_xpath)))
            
            print("Botão 'Atividades' encontrado. Clicando via JavaScript...")
            self.driver.execute_script("arguments[0].click();", botao_atividades)
            
            print("Botão 'Atividades' clicado com sucesso.")
            
            print("Aguardando a janela de atividades...")
            seletor_linhas = "tr[ng-repeat*='disciplAtividadesList']"
            linhas_atividades = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor_linhas)))
            print(f"Encontradas {len(linhas_atividades)} disciplinas na lista.")

            for linha in linhas_atividades:
                nome_disciplina = linha.find_element(By.CSS_SELECTOR, "div.font-montserrat span.ng-binding").text
                status = ""
                prazo = "N/A"
                try:
                    status = linha.find_element(By.CSS_SELECTOR, "span.text-danger").text
                    prazo_bruto = linha.find_element(By.CSS_SELECTOR, "span.hint-text").text
                    prazo = prazo_bruto.replace("|", "").strip()
                except NoSuchElementException:
                    status = linha.find_element(By.CSS_SELECTOR, "span.text-primary").text
                dados_disciplina = {"disciplina": nome_disciplina, "status": status, "prazo": prazo}
                atividades.append(dados_disciplina)
            
            botao_fechar = self.driver.find_element(By.CSS_SELECTOR, "button.bnt-close-dialog")
            self.driver.execute_script("arguments[0].click();", botao_fechar)

        except Exception as e:
            print(f"Ocorreu um erro ao checar as atividades: {e}")
        
        print("Verificação de atividades concluída.")
        return atividades

    def close(self):
        print("Fechando o scraper.")
        self.driver.quit()