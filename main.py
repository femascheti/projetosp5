from flask import Flask, render_template, request
# from celery_worker import fetch_project_info  # Importa a tarefa do Celery
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


app = Flask(__name__,static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    project_info = None
    error_message = None
    driver = None
    
    if request.method == 'POST':
        link = request.form.get('link')
        
        try:
            base_url = "https://editor.p5js.org/"
            username = link.split("/")[3]
            user_sketches_url = f"{base_url}{username}/sketches"
            
            # Configurando o Selenium em modo headless
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(user_sketches_url)
            time.sleep(30) 
            
            # Encontrar a tabela
            table = driver.find_element(By.CLASS_NAME, 'sketches-table')
            project_row = None
            for row in table.find_elements(By.CLASS_NAME, 'sketches-table__row'):
                project_link = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if project_link == link:
                    project_row = row
                    break

            if project_row:
                project_name = row.find_element(By.TAG_NAME, 'a').text
                creation_date = project_row.find_elements(By.TAG_NAME, 'td')[0].text  # Data de criação
                modification_date = project_row.find_elements(By.TAG_NAME, 'td')[1].text  # Data de modificação
                
                project_info = {
                    'name': project_name,
                    'link': project_link,
                    'creation_date': creation_date,
                    'modification_date': modification_date,
                }
            else:
                error_message = "Projeto não encontrado."
        
        except Exception as e:
            error_message = f"Ocorreu um erro: {e}"
        
        finally:
            if driver:
                driver.quit()  # Fecha o navegador

    return render_template('index.html', project_info=project_info, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
