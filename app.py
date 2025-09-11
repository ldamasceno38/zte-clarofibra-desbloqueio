import streamlit as st
import tempfile
import os
import subprocess
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# Configuration - UPDATE THESE PATHS
ZTE_UTILITY_PATH = os.path.dirname(os.path.abspath(__file__))  # Path to your cloned repo
EXAMPLES_PATH = ZTE_UTILITY_PATH

# Add custom CSS matching the HTML design
def add_custom_css():
    st.markdown("""
    <style>
    /* Import Fira Code font for a modern dev look */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main App and Background Styling */
    .stApp {
        background: #0d0d0d !important;
        color: #e0e0e0 !important;
        font-family: 'Fira Code', monospace !important;
        line-height: 1.8; /* Increased line height for better readability */
    }
    
    .main {
        background: #0d0d0d !important;
        color: #e0e0e0 !important;
    }
    
    /* Animated Stars Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #4a4a4a, transparent),
            radial-gradient(2px 2px at 40px 70px, #e0e0e0, transparent),
            radial-gradient(1px 1px at 90px 40px, #4a4a4a, transparent),
            radial-gradient(1px 1px at 130px 80px, #e0e0e0, transparent),
            radial-gradient(2px 2px at 160px 30px, #4a4a4a, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: stars 20s linear infinite;
    }
    
    @keyframes stars {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-100px); }
    }
    
    /* Header Styling with Glow Effect */
    h1 {
        font-size: 2.8rem !important; /* Slightly larger for emphasis */
        font-weight: 700 !important;
        color: #fff !important;
        text-align: center !important;
        text-shadow: 0 0 20px #fff !important;
        animation: glow 2s ease-in-out infinite alternate !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Fira Code', monospace !important;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #fff; }
        to { text-shadow: 0 0 30px #aaa, 0 0 40px #fff; }
    }
    
    /* Tagline Styling */
    .tagline {
        font-size: 1.1rem;
        color: #aaa;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Fira Code', monospace;
    }
    
    /* Main Container Styling (The Card) */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        margin: 1rem auto !important;
        backdrop-filter: blur(10px);
        max-width: 900px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* Description Box */
    .description {
        background: rgba(255, 255, 255, 0.08) !important;
        border-left: 4px solid #f5a623 !important; /* Golden accent line */
        padding: 1.5rem !important;
        margin-bottom: 3rem !important;
        border-radius: 0 8px 8px 0 !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 6px !important;
        color: #fff !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #ffd700 !important; /* Golden focus color */
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888 !important;
    }
    
    /* Labels */
    .stTextInput > label,
    .stSelectbox > label {
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        font-family: 'Fira Code', monospace !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 2rem !important;
    }
    
    .stFileUploader > div > div > div {
        color: #fff !important;
        font-family: 'Fira Code', monospace !important;
        font-weight: 400 !important;
    }
    
    /* Primary Button - Golden Gradient */
    .stButton > button[data-testid="baseButton-primary"] {
        width: 100% !important;
        padding: 1rem !important;
        background: linear-gradient(45deg, #f5a623, #f7d75d) !important;
        border: 2px solid #f5a623 !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(45deg, #f7d75d, #f9e285) !important;
        box-shadow: 0 0 20px rgba(245, 166, 35, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Regular Buttons - White Gradient */
    .stButton > button:not([data-testid="baseButton-primary"]) {
        width: 100% !important;
        padding: 1rem !important;
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.2)) !important;
        border: 2px solid #ccc !important;
        border-radius: 8px !important;
        color: #fff !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:not([data-testid="baseButton-primary"]):hover {
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.3)) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Download Button Special Styling (Same as primary) */
    .stDownloadButton > button {
        width: 100% !important;
        padding: 1rem !important;
        background: linear-gradient(45deg, #f5a623, #f7d75d) !important;
        border: 2px solid #f5a623 !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(45deg, #f7d75d, #f9e285) !important;
        box-shadow: 0 0 20px rgba(245, 166, 35, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Alert Messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        font-family: 'Fira Code', monospace !important;
    }
    
    .stSuccess {
        background: rgba(30, 150, 30, 0.2) !important;
        border-left: 4px solid #4CAF50 !important;
        color: #b0e0b0 !important;
    }
    
    .stError {
        background: rgba(200, 50, 50, 0.2) !important;
        border-left: 4px solid #f44336 !important;
        color: #ffb0b0 !important;
    }
    
    .stInfo {
        background: rgba(60, 140, 200, 0.2) !important;
        border-left: 4px solid #2196F3 !important;
        color: #a0c0ff !important;
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.2) !important;
        border-left: 4px solid #ff9800 !important;
        color: #ffe0b2 !important;
    }
    
    /* Code Blocks */
    .stCode {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 6px !important;
        padding: 1.5rem !important;
        color: #32cd32 !important; /* A brighter lime green */
        font-family: 'Fira Code', monospace !important;
        font-size: 0.9rem !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        color: #fff !important;
    }
    
    /* Section Titles */
    .section-title {
        font-size: 1.5rem !important;
        color: #fff !important;
        margin-bottom: 1.5rem !important;
        border-left: 4px solid #ffd700 !important; /* Golden accent */
        padding-left: 1rem !important;
        font-family: 'Fira Code', monospace !important;
        font-weight: 700 !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Markdown styling */
    .stMarkdown {
        color: #e0e0e0 !important;
        font-family: 'Fira Code', monospace !important;
    }
    
    .stMarkdown a {
        color: #f7d75d !important; /* Lighter golden for links */
        text-decoration: none !important;
    }
    
    .stMarkdown a:hover {
        color: #fff !important;
        text-decoration: underline !important;
    }
    
    /* Fade in animation for content */
    .stApp > div {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

# Add the rest of the app.py code below this function
def setup_python_path():
    """Ensure the ZTE utility path is in PYTHONPATH for subprocess calls"""
    current_path = os.environ.get('PYTHONPATH', '')
    zte_path = os.path.abspath(ZTE_UTILITY_PATH)
    
    if zte_path not in current_path:
        if current_path:
            os.environ['PYTHONPATH'] = f"{zte_path}:{current_path}"
        else:
            os.environ['PYTHONPATH'] = zte_path

def editar_header_arquivo(caminho_arquivo):
    """Correct the header bytes in the .bin file"""
    try:
        if not os.path.exists(caminho_arquivo) or not os.path.isfile(caminho_arquivo):
            return False

        with open(caminho_arquivo, 'rb') as arquivo:
            dados = bytearray(arquivo.read())

        if len(dados) < 154:
            return False

        with open(caminho_arquivo + ".backup", 'wb') as backup:
            backup.write(dados)
        
        # Alteração de Bytes Específicos no Header
        # Byte 0x40 -> Valor 02
        # Byte 0x99 -> Valor 06
        dados[0x40] = 0x02
        dados[0x99] = 0x06

        with open(caminho_arquivo, 'wb') as arquivo:
            arquivo.write(dados)

        return True

    except Exception as e:
        st.error(f"❌ Erro ao corrigir header: {str(e)}")
        return False

def main():
    st.set_page_config(
        page_title="ZTE Tools Suite - Desbloqueio Claro",
        page_icon="🔓",
        layout="wide"
    )
    
    # Apply custom CSS
    add_custom_css()
    
    # Main header with glow effect
    st.markdown('<h1>🔓 ZTE CLARO FTTH 🔓</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Habilita permissões ADMIN para o usuário da Etiqueta</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">by github.com/ldamasceno38 using binaries from mkst/zte-config-utility</p>', unsafe_allow_html=True)

    
    # Setup Python path for subprocesses
    setup_python_path()
    
    # Check if paths exist
    if not check_paths():
        return
    
    # Main interface
    process_interface()

def check_paths():
    """Check if required paths exist"""
    auto_script = os.path.join(EXAMPLES_PATH, "auto.py")
    encode_script = os.path.join(EXAMPLES_PATH, "encode.py")
    
    if not os.path.exists(auto_script):
        st.error(f"❌ auto.py não encontrado em: {auto_script}")
        st.info("Por favor, atualize a variável ZTE_UTILITY_PATH no script")
        st.code(f"""
# Atualize este caminho para apontar para seu diretório zte-config-utility:
ZTE_UTILITY_PATH = "/caminho/para/seu/zte-config-utility"

# Configuração atual: {ZTE_UTILITY_PATH}
# Caminho absoluto: {os.path.abspath(ZTE_UTILITY_PATH)}
        """)
        return False
    
    return True

def run_script_with_env(cmd, cwd=None):
    """Run a script with proper environment setup and filter output"""
    import sys
    
    env = os.environ.copy()
    zte_path = os.path.abspath(ZTE_UTILITY_PATH)
    
    # Get current Python paths from the running environment
    current_paths = sys.path.copy()
    
    # Add ZTE path
    if zte_path not in current_paths:
        current_paths.append(zte_path)
    
    # Set PYTHONPATH to include all current paths
    env['PYTHONPATH'] = os.pathsep.join(current_paths)
    
    # Also ensure we use the same Python executable
    if cmd[0] == 'python3':
        cmd[0] = sys.executable
    elif cmd[0] == 'python':
        cmd[0] = sys.executable
    
    # Run with suppressed stdout to avoid debug output
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env)
    
    # Filter out unwanted debug lines from stdout
    if result.stdout:
        filtered_lines = []
        for line in result.stdout.split('\n'):
            # Skip lines that contain debug info we don't want to show
            if any(skip_text in line for skip_text in [
                'Using Python:',
                'PYTHONPATH:',
                'python3',
                '/home/adminuser',
                '/usr/local/lib'
            ]):
                continue
            if line.strip():  # Only keep non-empty lines
                filtered_lines.append(line)
        
        # Reconstruct stdout without debug lines
        result.stdout = '\n'.join(filtered_lines)
    
    return result

def modify_xml_auth_level(xml_content):
    """Modify XML to set DevAuthInfo Level to 1 on Row 2"""
    try:
        root = ET.fromstring(xml_content)
        modified = False
        for table in root.findall(".//Tbl[@name='DevAuthInfo']"):
            for row in table.findall("Row[@No='1']"):
                for dm in row.findall("DM[@name='Level']"):
                    old_value = dm.get('val', 'N/A')
                    dm.set('val', '1')
                    st.success("✅ **Interface Desbloqueada com Sucesso!**")
                    modified = True
                    break
                break
            break
        
        if not modified:
            st.warning("⚠️ Tabela DevAuthInfo ou Row 2 não encontrada no XML")
            return xml_content
        
        modified_xml = ET.tostring(root, encoding='unicode')
        return modified_xml
        
    except Exception as e:
        st.error(f"❌ Erro ao modificar XML: {str(e)}")
        return xml_content

def process_interface():
    """Interface for processing config.bin with ZTE Tools Suite styling"""
    
    st.markdown("### Carregue seu config.bin e preencha as informações")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📁 Arraste e solte o arquivo config.bin",
        type=["bin"],
        help="Selecione o arquivo config.bin do seu roteador ZTE"
    )
    
    # Create two columns for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        mac = st.text_input(
            "🌐 Endereço MAC - Etiqueta ONT-MAC",
            placeholder="AA:BB:CC:DD:EE:FF",
            help="Endereço MAC do roteador"
        )
        serial = st.text_input(
            "🔢 Número de Série - Etiqueta PON-SN",
            placeholder="ZTEXXXXXXXXXXXX",
            help="Número de série do roteador"
        )
    
    with col2:
        signature = st.selectbox(
            "📡 Modelo da ONT",
            options=["F6600P", "F6645P"],
            help="Selecione o modelo do seu roteador"
        )
        
        # Add some spacing
        st.write("")
    
    # Process button
    if st.button("🔓 DESBLOQUEAR INTERFACE", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("❌ Por favor, carregue um arquivo config.bin")
            return
        
        # Add processing status
        with st.status("🚀 Processando arquivo...", expanded=True) as status:
            process_file_with_status(uploaded_file, serial, mac, signature, status)

def process_file_with_status(uploaded_file, serial, mac, signature, status):
    """Process config.bin with status updates"""
    try:
        # Step 1: Decode
        status.write("🔍 Decodificando arquivo config.bin...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as tmp_input:
            tmp_input.write(uploaded_file.getvalue())
            input_path = tmp_input.name
        
        output_xml_path = input_path.replace('.bin', '.xml')
        
        auto_script = os.path.join(EXAMPLES_PATH, "auto.py")
        cmd = ['python3', auto_script, input_path, output_xml_path]
        
        if serial:
            cmd.extend(['--serial', serial])
        if mac:
            cmd.extend(['--mac', mac])
        
        result = run_script_with_env(cmd, cwd=ZTE_UTILITY_PATH)
        
        if result.returncode != 0:
            status.update(label="❌ Falha na decodificação", state="error")
            st.error("❌ Falha na decodificação")
            if result.stderr:
                st.error("**Detalhes do erro:**")
                st.code(result.stderr)
            if result.stdout:
                st.info("**Saída do script:**")
                st.text(result.stdout)
            st.info("💡 **Sugestões para solução de problemas:**")
            st.markdown("""
            - **Para payloads 'mac'**: Forneça o Endereço MAC (AA:BB:CC:DD:EE:FF)
            - **Para payloads 'serial'**: Forneça o Número de Série (ZTEXXXXXXXXXXXX)  
            - **Para payloads 'mac+serial'**: Forneça tanto MAC quanto Serial
            """)
            return
        
        # Extract key and IV info
        detected_key = None
        detected_iv = None
        if result.stdout:
            pattern = r"using \(key, iv\): \('([^']+)', '([^']+)'\)"
            match = re.search(pattern, result.stdout)
            if match:
                detected_key = match.group(1)
                detected_iv = match.group(2)
                status.write(f"🔑 Chave detectada: `{detected_key}` | IV: `{detected_iv}`")
        
        if not os.path.exists(output_xml_path):
            status.update(label="❌ Arquivo XML não encontrado", state="error")
            st.error("❌ Arquivo XML de saída não encontrado")
            return
        
        with open(output_xml_path, 'r', encoding='utf-8', errors='ignore') as f:
            xml_content = f.read()
        
        # Step 2: Modify XML
        status.write("✏️ Modificando configuração XML para desbloquear interface...")
        modified_xml = modify_xml_auth_level(xml_content)
        modified_xml_path = output_xml_path.replace('.xml', '_modified.xml')
        with open(modified_xml_path, 'w', encoding='utf-8') as f:
            f.write(modified_xml)
        
        # Step 3: Encode
        status.write("🔒 Codificando arquivo modificado...")
        output_bin_path = modified_xml_path.replace('.xml', '.bin')
        encode_script = os.path.join(EXAMPLES_PATH, "encode.py")
        cmd = ['python3', encode_script, modified_xml_path, output_bin_path]
        
        if detected_key:
            cmd.extend(['--key', detected_key])
        if detected_iv:
            cmd.extend(['--iv', detected_iv])
        if signature:
            cmd.extend(['--signature', signature])
        
        cmd.append('--include-header')
        cmd.append('--little-endian-header')
        
        result = run_script_with_env(cmd, cwd=ZTE_UTILITY_PATH)
        
        if result.returncode != 0:
            status.update(label="❌ Falha na codificação", state="error")
            st.error("❌ Falha na codificação")
            if result.stderr:
                st.error("**Detalhes do erro:**")
                st.code(result.stderr)
            if result.stdout:
                st.info("**Saída do script:**")
                st.text(result.stdout)
            return
        
        if not os.path.exists(output_bin_path):
            status.update(label="❌ Arquivo bin não encontrado", state="error")
            st.error("❌ Arquivo bin de saída não encontrado")
            return
        
        # Step 4: Fix header
        status.write("🔧 Corrigindo header do arquivo...")
        if not editar_header_arquivo(output_bin_path):
            status.update(label="❌ Falha ao corrigir header", state="error")
            st.error("❌ Falha ao corrigir header do arquivo")
            return
        
        # Step 5: Prepare download
        status.write("📦 Preparando arquivo para download...")
        with open(output_bin_path, 'rb') as f:
            encoded_data = f.read()
        
        status.update(label="🎉 Desbloqueio concluído com sucesso!", state="complete")
        
        # Success message and download button
        st.success("🎉 **Desbloqueio concluído com sucesso!**")
        st.info("📋 **O que foi feito:**\n- Decodificação do config.bin\n- Modificação do nível de autorização\n- Recodificação com header corrigido")
        
        st.download_button(
            label="⬇️ BAIXAR CONFIG.BIN DESBLOQUEADO",
            data=encoded_data,
            file_name="config_desbloqueado.bin",
            mime="application/octet-stream",
            type="primary",
            use_container_width=True
        )
        
    except Exception as e:
        status.update(label=f"❌ Erro durante processamento", state="error")
        st.error(f"❌ Erro durante processamento: {str(e)}")
    
    finally:
        # Cleanup temporary files
        try:
            if 'input_path' in locals():
                os.unlink(input_path)
            if 'output_xml_path' in locals() and os.path.exists(output_xml_path):
                os.unlink(output_xml_path)
            if 'modified_xml_path' in locals() and os.path.exists(modified_xml_path):
                os.unlink(modified_xml_path)
            if 'output_bin_path' in locals() and os.path.exists(output_bin_path):
                os.unlink(output_bin_path)
        except:
            pass

def process_file(uploaded_file, serial, mac, signature):
    """Legacy function - now redirects to new status version"""
    pass  # This function is no longer used

if __name__ == "__main__":
    main()
