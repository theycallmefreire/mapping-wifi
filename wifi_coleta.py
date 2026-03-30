import subprocess
import re

def get_wifi_strength():
    """Pega a força do sinal Wi-Fi em porcentagem"""
    try:
        result = subprocess.run(
            'netsh wlan show interfaces',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        for line in result.stdout.split('\n'):
            if 'Sinal' in line:
                match = re.search(r'(\d+)', line)
                if match:
                    percentage = int(match.group(1))
                    return percentage
        
        return None
    except Exception as e:
        return None