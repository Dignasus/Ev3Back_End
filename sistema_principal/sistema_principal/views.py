import requests
from django.shortcuts import render, redirect

def login_view(request):
    mensaje = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        api_url = "http://127.0.0.1:8050/api/autentificar/"
        try:
            response = requests.post(api_url, json={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                if data.get("autorizado"):
                    # Guardar datos en sesión temporalmente
                    request.session['usuario'] = data.get("usuario")
                    request.session['menu_opciones'] = data.get("menu_opciones")
                    return redirect('home')
            mensaje = "Credenciales incorrectas o acceso denegado por la API."
        except requests.exceptions.ConnectionError:
            mensaje = "Error de conexión: La API (8050) no está disponible."

    return render(request, 'login.html', {"mensaje": mensaje})

def home_view(request):
    usuario = request.session.get('usuario')
    menu_opciones = request.session.get('menu_opciones')
    
    if not usuario:
        return redirect('login')

    return render(request, 'index.html', {"usuario": usuario, "menu_opciones": menu_opciones})

def logout_view(request):
    request.session.flush()
    return redirect('login')