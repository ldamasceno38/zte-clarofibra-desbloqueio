import streamlit as st
import Cryptodome
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
    /* Import Courier New font and reset */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main background and body styling */
    .stApp {
        background: #0a0a0a !important;
        color: #f5f5f5 !important;
        font-family: 'Courier New', 'Courier Prime', monospace !important;
        line-height: 1.6;
    }
    
    .main {
        background: #0a0a0a !important;
        color: #f5f5f5 !important;
    }
    
    /* Animated stars background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #bbb, transparent),
            radial-gradient(2px 2px at 40px 70px, #fff, transparent),
            radial-gradient(1px 1px at 90px 40px, #bbb, transparent),
            radial-gradient(1px 1px at 130px 80px, #fff, transparent),
            radial-gradient(2px 2px at 160px 30px, #bbb, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: stars 20s linear infinite;
    }
    
    @keyframes stars {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-100px); }
    }
    
    /* Header styling with glow effect */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #fff !important;
        text-align: center !important;
        text-shadow: 0 0 20px #fff !important;
        animation: glow 2s ease-in-out infinite alternate !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Courier New', monospace !important;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #fff; }
        to { text-shadow: 0 0 30px #aaa, 0 0 40px #fff; }
    }
    
    /* Tagline styling */
    .tagline {
        font-size: 1.1rem;
        color: #aaa;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Courier New', monospace;
    }
    
    /* Main container styling */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        margin: 1rem auto !important;
        backdrop-filter: blur(10px);
        max-width: 800px !important;
    }
    
    /* Description box */
    .description {
        background: rgba(255, 255, 255, 0.1) !important;
        border-left: 4px solid #fff !important;
        padding: 1.5rem !important;
        margin-bottom: 3rem !important;
        border-radius: 0 8px 8px 0 !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 4px !important;
        color: #fff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #fff !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #666 !important;
    }
    
    /* Labels */
    .stTextInput > label,
    .stSelectbox > label {
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        font-family: 'Courier New', monospace !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.5) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stFileUploader > div > div > div {
        color: #fff !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Primary button - golden gradient */
    .stButton > button[data-testid="baseButton-primary"] {
        width: 100% !important;
        padding: 1rem !important;
        background: linear-gradient(45deg, #ffd700, #ffed4e) !important;
        border: 2px solid #ffd700 !important;
        border-radius: 8px !important;
        color: #000 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(45deg, #ffed4e, #fff700) !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Regular buttons - white gradient */
    .stButton > button:not([data-testid="baseButton-primary"]) {
        width: 100% !important;
        padding: 1rem !important;
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.4)) !important;
        border: 2px solid #fff !important;
        border-radius: 8px !important;
        color: #fff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:not([data-testid="baseButton-primary"]):hover {
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.6)) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        width: 100% !important;
        padding: 1rem !important;
        background: linear-gradient(45deg, #ffd700, #ffed4e) !important;
        border: 2px solid #ffd700 !important;
        border-radius: 8px !important;
        color: #000 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(45deg, #ffed4e, #fff700) !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Alert messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    .stSuccess {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #888 !important;
        color: #fff !important;
    }
    
    .stError {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #666 !important;
        color: #fff !important;
    }
    
    .stInfo {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #888 !important;
        color: #fff !important;
    }
    
    .stWarning {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #888 !important;
        color: #fff !important;
    }
    
    /* Code blocks */
    .stCode {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 4px !important;
        padding: 1rem !important;
        color: #32cd32 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Spinner */
    .stSpinner {
        color: #fff !important;
    }
    
    /* Section titles */
    .section-title {
        font-size: 1.5rem !important;
        color: #fff !important;
        margin-bottom: 1.5rem !important;
        border-left: 4px solid #fff !important;
        padding-left: 1rem !important;
        font-family: 'Courier New', monospace !important;
        font-weight: 700 !important;
    }
    
    /* Columns */
    .row-widget {
        background: transparent !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Markdown styling */
    .stMarkdown {
        color: #f5f5f5 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    .stMarkdown a {
        color: #ffd700 !important;
        text-decoration: none !important;
    }
    
    .stMarkdown a:hover {
        color: #fff700 !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        
        .block-container {
            padding: 1rem !important;
            margin: 0.5rem !important;
        }
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

# Add the ZTE utility path to Python path for subprocess calls
def setup_python_path():
    """Ensure the ZTE utility path is in PYTHONPATH for subprocesses"""
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
        page_title="Desbloqueio ZTE Claro Fibra",
        page_icon="🔓",
        layout="wide"
    )
    
    # Apply custom CSS
    add_custom_css()
    
    # Main header with glow effect
    st.markdown('<h1>Desbloqueio ZTE Claro Fibra</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Habilita funções ADMIN no Usuário da Etiqueta</p>', unsafe_allow_html=True)
    st.markdown('<strong>Feito por:</strong> <a href="https://github.com/ldamasceno38" target="_blank">https://github.com/ldamasceno38</a>', unsafe_allow_html=True)
    st.markdown('Fork de:</strong> <a href="https://github.com/mkst/zte-config-utility" target="_blank">https://github.com/mkst/zte-config-utility</a>', unsafe_allow_html=True)

    
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
    """Run a script with proper environment setup"""
    env = os.environ.copy()
    zte_path = os.path.abspath(ZTE_UTILITY_PATH)
    current_pythonpath = env.get('PYTHONPATH', '')
    
    if current_pythonpath:
        env['PYTHONPATH'] = f"{zte_path}:{current_pythonpath}"
    else:
        env['PYTHONPATH'] = zte_path
    
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env)

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
            "🌐 Endereço MAC (Etiqueta ONT MAC)",
            placeholder="AA:BB:CC:DD:EE:FF",
            help="Endereço MAC do roteador"
        )
        serial = st.text_input(
            "🔢 Número de Série (Etiqueta PON-SN)",
            placeholder="ZTEGXXXXXXXX",
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
