# scraper/studeo_scraper.py

# MUDANÇA 1: Não precisamos mais do webdriver-manager aqui
from selenium.webdriver.edge.service import Service 
from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class StudeoScraper:
    # MUDANÇA 2: O __init__ agora recebe o caminho do driver como um argumento
    def __init__(self, driver_path: str):
        
        # MUDANÇA 3: Usamos o caminho fornecido para inicializar o Service
        service = Service(executable_path=driver_path)
        
        self.driver = EdgeDriver(service=service)
        self.wait = WebDriverWait(self.driver, 10)
        print("Scraper para Microsoft Edge inicializado com driver manual.")

    # O resto do arquivo (def login, def close) continua exatamente igual
    
    def login(self, cpf, senha):
        """
        Executa o processo completo de login no Studeo.
        """
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
            
            print("Aguardando a página de seleção de modalidade...")
            print("Login completo! (Aguardando o seletor do botão 'Acessar' para automatizar 100%)")
            time.sleep(10)
            return True

        except Exception as e:
            print(f"Ocorreu um erro durante o login: {e}")
            return False

    def close(self):
        """
        Fecha o navegador.
        """
        print("Fechando o scraper.")
        self.driver.quit()