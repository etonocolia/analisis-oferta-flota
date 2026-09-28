# 📋 Guía de Despliegue - Aplicación de Análisis de Oferta No Cubierta

## 🚀 Opción 3: Streamlit Cloud (Acceso desde cualquier lugar)

Esta guía te permitirá desplegar la aplicación en la nube para que pueda ser accesible desde cualquier dispositivo con conexión a internet.

---

## 📋 Requisitos Previos

- Cuenta de GitHub (gratuita): https://github.com
- Cuenta de Streamlit Cloud (gratuita): https://share.streamlit.io
- Archivos en tu computadora:
  - `app_analisis_oferta.py` (código principal)
  - `OfertaFlotaNoCubierta.xlsx` (archivo de datos)

---

## 📝 Paso a Paso

### **Paso 1: Crear cuenta en GitHub**

1. Ve a https://github.com
2. Haz clic en **"Sign up"** (Registrarse)
3. Ingresa tu correo electrónico
4. Crea una contraseña segura
5. Verifica tu correo electrónico

---

### **Paso 2: Crear un nuevo repositorio**

1. En GitHub, haz clic en el botón **"+"** (esquina superior derecha)
2. Selecciona **"New repository"**
3. Configura el repositorio:
   - **Repository name:** `analisis-oferta-flota`
   - **Description:** `Aplicación de análisis de oferta de flota no cubierta`
   - **Visibility:** `Private` (recomendado) o `Public`
4. Haz clic en **"Create repository"**

---

### **Paso 3: Subir los archivos al repositorio**

#### **Opción A: Desde la interfaz web de GitHub**

1. En tu nuevo repositorio, haz clic en **"uploading an existing file"**
2. Arrastra o selecciona los archivos:
   - `app_analisis_oferta.py`
   - `OfertaFlotaNoCubierta.xlsx`
3. Escribe un mensaje de commit: `Versión inicial de la aplicación`
4. Haz clic en **"Commit changes"**

#### **Opción B: Desde la terminal (más rápido)**

```bash
# Navegar a la carpeta del proyecto
cd C:\Users\usuario\Documents

# Inicializar repositorio Git
git init

# Agregar archivos
git add app_analisis_oferta.py OfertaFlotaNoCubierta.xlsx

# Crear commit
git commit -m "Versión inicial de la aplicación"

# Conectar con GitHub (reemplaza TU_USUARIO)
git branch -M main
git remote add origin https://github.com/TU_USUARIO/analisis-oferta-flota.git

# Subir archivos
git push -u origin main
```

---

### **Paso 4: Crear cuenta en Streamlit Cloud**

1. Ve a https://share.streamlit.io
2. Haz clic en **"Sign up"**
3. Selecciona **"Continue with GitHub"** (recomendado)
4. Autoriza la aplicación
5. Completa tu perfil

---

### **Paso 5: Desplegar la aplicación**

1. En Streamlit Cloud, haz clic en **"New app"**
2. Configura el despliegue:
   - **Repository:** Selecciona `analisis-oferta-flota`
   - **Branch:** `main`
   - **Main file path:** `app_analisis_oferta.py`
3. Haz clic en **"Deploy"**

⏱️ **Tiempo estimado:** 2-5 minutos

---

### **Paso 6: Configurar secretos (opcional)**

Si necesitas variables de entorno o credenciales:

1. En la página de tu app, haz clic en **"Settings"** ⚙️
2. Selecciona **"Secrets"**
3. Agrega las variables necesarias en formato TOML:
   ```toml
   MI_VARIABLE = "valor"
   ```
4. Haz clic en **"Save"**

---

### **Paso 7: Acceder a tu aplicación**

Una vez desplegada, tu aplicación estará disponible en:

```
https://TU_USUARIO-streamlit-analisis-oferta-flota-XXXXXX.streamlit.app
```

**Comparte esta URL** con tu Gerente o equipo para que accedan desde cualquier lugar.

---

## 🔧 Solución de Problemas

### **Error: "ModuleNotFoundError"**

Si falta una librería, crea un archivo `requirements.txt` en tu repositorio:

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
openpyxl>=3.1.0
```

Sube este archivo al repositorio y Streamlit instalará las dependencias automáticamente.

### **Error: "FileNotFoundError"**

Verifica que el archivo Excel esté en el repositorio y que el nombre coincida exactamente con el código:

```python
df = pd.read_excel('OfertaFlotaNoCubierta.xlsx', sheet_name='ConsolidadoNoCumplidos')
```

### **Error: "Permission denied"**

Si el repositorio es privado, asegúrate de:
1. Haber iniciado sesión en GitHub
2. Tener permisos de acceso al repositorio

---

## 🔄 Actualizaciones

Cuando actualices el código o los datos:

1. Modifica los archivos en tu repositorio
2. Haz commit y push:
   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   git push
   ```
3. Streamlit Cloud **actualizará automáticamente** tu aplicación en 1-2 minutos

---

## 📊 Opciones de Streamlit Cloud

| Plan | Precio | Características |
|------|--------|-----------------|
| **Community** | Gratis | Apps públicas, 1 GB RAM, comunidad |
| **Pro** | $20/mes | Apps privadas, más recursos |
| **Enterprise** | Personalizado | Soporte dedicado, SSO |

---

## 🎯 Resumen de Archivos Necesarios

```
C:\Users\usuario\Documents\
├── app_analisis_oferta.py          # Código principal
├── OfertaFlotaNoCubierta.xlsx      # Datos
├── requirements.txt                 # Dependencias (recomendado)
└── GUIA_DESPLIEGUE.md              # Esta guía
```

---

## ✅ Checklist Final

- [ ] Cuenta de GitHub creada
- [ ] Repositorio creado
- [ ] Archivos subidos (`app_analisis_oferta.py` y `OfertaFlotaNoCubierta.xlsx`)
- [ ] Cuenta de Streamlit Cloud creada
- [ ] Aplicación desplegada
- [ ] URL de acceso probada
- [ ] URL compartida con el Gerente

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa la documentación oficial: https://docs.streamlit.io
2. Consulta la comunidad: https://discuss.streamlit.io
3. Revisa los logs en Streamlit Cloud para identificar errores

---

**Última actualización:** Septiembre 2026
