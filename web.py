import tkinter as tk
from tkinter import Tk, messagebox
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
import time
import os

 # URL de la página de inicio de sesión
url_inicio_sesion = "https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi"
    
# URL de la página después del inicio de sesión
url_pagina_principal = "https://www1.sii.cl/cgi-bin/Portal001/mipeSelEmpresa.cgi?DESDE_DONDE_URL=OPCION%3D33%26TIPO%3D4"

url_pagina_despacho = "https://www1.sii.cl/cgi-bin/Portal001/mipeLaunchPage.cgi?OPCION=52&TIPO=4"    

def Facturar(rut_receptor, dv_receptor, nombre_producto_, cantidad_,precio_,descripcion=None):
    
    
    rut = "115147684"
    clave = "7513"
    chrome_driver_path = r"C:\Users\yerko\Desktop\Proyecto\python\chromedriver-win64\chromedriver.exe"

    driver = None

    try:
        driver = webdriver.Chrome()

        # Abre una página web en el navegador
        driver.get(url_inicio_sesion)

        # Localiza los elementos del formulario y completa los campos
        rut_field = driver.find_element(By.CSS_SELECTOR, "input#rutcntr")
        clave_field = driver.find_element(By.CSS_SELECTOR, "input#clave")

        rut_field.send_keys(rut)
        clave_field.send_keys(clave)

        login_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.ID, "bt_ingresar"))
        )
        login_button.click()



        try:
            alert = driver.switch_to.alert
            alert.dismiss()  # Cierra la alerta haciendo clic en el botón "Cancelar" o "Cerrar"
            print("Alerta cerrada exitosamente.")
        except Exception as e:
            print(f"No se pudo cerrar la alerta: {e}")


      
        # Navega a la nueva página con la sesión iniciada
        driver.get(url_pagina_despacho)

        
        empresa_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))
        )
        empresa_button.click()

        rut_receptor_field = WebDriverWait(driver, 11).until(
            EC.presence_of_element_located((By.NAME, "EFXP_RUT_RECEP"))
        )
        rut_receptor_field.send_keys(rut_receptor)


        dv_receptor_field = WebDriverWait(driver, 11).until(
            EC.presence_of_element_located((By.NAME, "EFXP_DV_RECEP"))
        )

        # Ingresa el valor en el campo de DV receptor
        dv_receptor_field.send_keys(dv_receptor)
        dv_receptor_field.send_keys(Keys.RETURN)


        campo_ciudad = driver.find_element(By.NAME, "EFXP_CIUDAD_RECEP")
        if not campo_ciudad.get_attribute("value"):
            # Si está vacío, llena el campo de ciudad con un dato
            campo_ciudad.send_keys("Alto Hospicio")


        nombre_producto = driver.find_element(By.NAME, "EFXP_NMB_01")
        nombre_producto.send_keys(nombre_producto_)

        time.sleep(0.5)
        
        cantidad = driver.find_element(By.NAME, "EFXP_QTY_01")
        cantidad.send_keys(cantidad_)  # Aquí puedes ingresar la cantidad que desees
        
        time.sleep(0.5)
        
        # Precio
        precio = driver.find_element(By.NAME, "EFXP_PRC_01")
        precio.send_keys(precio_)  # Aquí puedes ingresar el precio que desees

        time.sleep(0.5)

        if descripcion:
            print("tengo el texto es:", descripcion)
            
            # Marca la casilla de ticket (checkbox)
            casilla_ticket = driver.find_element(By.NAME, "DESCRIP_01")
            if not casilla_ticket.is_selected():
                casilla_ticket.click()

            # Ingresa la descripción en el campo correspondiente
            descripcion_field = driver.find_element(By.NAME, "EFXP_DSC_ITEM_01")
            
            # Borra cualquier texto existente en el campo
            descripcion_field.clear()
            
            # Ingresa la nueva descripción
            descripcion_field.send_keys(descripcion)

        validar_y_visualizar_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='Button_Update']"))
        )
        validar_y_visualizar_button.click()


        firma_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.NAME, 'btnSign'))
        )

        firma_button.click()


        firma_button2 = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.ID, 'btnFirma'))
        )

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'myPass'))
        )

        password_field.send_keys('Xd')

        print("esta lista para firmar,")
        time.sleep(120)

    except UnexpectedAlertPresentException:
    # Maneja la excepción de la alerta emergente aquí si es necesario
        print("Se detectó una alerta emergente, maneja esta situación si es necesario.")
    # Puedes cerrar la alerta si es posible
    try:
        alert = Alert(driver)
        alert.accept()
    except Exception as e:
        print(f"No se pudo manejar la alerta: {e}")

    finally:
        if driver:
            driver.quit()

def despacho(rut_receptor, dv_receptor, nombre_producto_, cantidad_,precio_,descripcion=None):
    
    
    rut = "115147684"
    clave = "7513"
    chrome_driver_path = r"C:\Users\yerko\Desktop\Proyecto\python\chromedriver-win64\chromedriver.exe"

    driver = None

    try:
        driver = webdriver.Chrome()

        # Abre una página web en el navegador
        driver.get(url_inicio_sesion)

        # Localiza los elementos del formulario y completa los campos
        rut_field = driver.find_element(By.CSS_SELECTOR, "input#rutcntr")
        clave_field = driver.find_element(By.CSS_SELECTOR, "input#clave")

        rut_field.send_keys(rut)
        clave_field.send_keys(clave)

        login_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.ID, "bt_ingresar"))
        )
        login_button.click()



        try:
            alert = driver.switch_to.alert
            alert.dismiss()  # Cierra la alerta haciendo clic en el botón "Cancelar" o "Cerrar"
            print("Alerta cerrada exitosamente.")
        except Exception as e:
            print(f"No se pudo cerrar la alerta: {e}")


      
        # Navega a la nueva página con la sesión iniciada
        driver.get(url_pagina_despacho)

        
        empresa_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))
        )
        empresa_button.click()

        rut_receptor_field = WebDriverWait(driver, 11).until(
            EC.presence_of_element_located((By.NAME, "EFXP_RUT_RECEP"))
        )
        rut_receptor_field.send_keys(rut_receptor)


        dv_receptor_field = WebDriverWait(driver, 11).until(
            EC.presence_of_element_located((By.NAME, "EFXP_DV_RECEP"))
        )

        # Ingresa el valor en el campo de DV receptor
        dv_receptor_field.send_keys(dv_receptor)
        dv_receptor_field.send_keys(Keys.RETURN)


        campo_ciudad = driver.find_element(By.NAME, "EFXP_CIUDAD_RECEP")
        if not campo_ciudad.get_attribute("value"):
            # Si está vacío, llena el campo de ciudad con un dato
            campo_ciudad.send_keys("Alto Hospicio")


        nombre_producto = driver.find_element(By.NAME, "EFXP_NMB_01")
        nombre_producto.send_keys(nombre_producto_)

        time.sleep(0.5)
        
        cantidad = driver.find_element(By.NAME, "EFXP_QTY_01")
        cantidad.send_keys(cantidad_)  # Aquí puedes ingresar la cantidad que desees
        
        time.sleep(0.5)
        
        # Precio
        precio = driver.find_element(By.NAME, "EFXP_PRC_01")
        precio.send_keys(precio_)  # Aquí puedes ingresar el precio que desees

        time.sleep(0.5)

        if descripcion:
            print("tengo el texto es:", descripcion)
            
            # Marca la casilla de ticket (checkbox)
            casilla_ticket = driver.find_element(By.NAME, "DESCRIP_01")
            if not casilla_ticket.is_selected():
                casilla_ticket.click()

            # Ingresa la descripción en el campo correspondiente
            descripcion_field = driver.find_element(By.NAME, "EFXP_DSC_ITEM_01")
            
            # Borra cualquier texto existente en el campo
            descripcion_field.clear()
            
            # Ingresa la nueva descripción
            descripcion_field.send_keys(descripcion)

        validar_y_visualizar_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='Button_Update']"))
        )
        validar_y_visualizar_button.click()


        firma_button = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.NAME, 'btnSign'))
        )

        firma_button.click()


        firma_button2 = WebDriverWait(driver, 11).until(
            EC.element_to_be_clickable((By.ID, 'btnFirma'))
        )

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'myPass'))
        )

        password_field.send_keys('Xd')

        print("esta lista para firmar,")
        time.sleep(60)

    except UnexpectedAlertPresentException:
    # Maneja la excepción de la alerta emergente aquí si es necesario
        print("Se detectó una alerta emergente, maneja esta situación si es necesario.")
    # Puedes cerrar la alerta si es posible
    try:
        alert = Alert(driver)
        alert.accept()
    except Exception as e:
        print(f"No se pudo manejar la alerta: {e}")

    finally:
        if driver:
            driver.quit()

def iniciar_facturar(rut_receptor, dv_receptor, producto_nombre, cantidad,precio, descripcion=None):
    # Crea un hilo para ejecutar la función Facturar

    thread = Thread(target=Facturar, args=(rut_receptor, dv_receptor, producto_nombre, cantidad,precio,descripcion))
    
    
    # Inicia el hilo
    thread.start()

def iniciar_despacho(rut_receptor, dv_receptor, producto_nombre, cantidad,precio, descripcion=None):
    # Crea un hilo para ejecutar la función Facturar

    thread = Thread(target=despacho, args=(rut_receptor, dv_receptor, producto_nombre, cantidad,precio,descripcion))
    
    # Inicia el hilo
    thread.start()    



def mostrar_mensaje():
    # Muestra el mensaje "Factura Terminada"
    messagebox.showinfo("Factura Terminada", "Factura terminada!")



