
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
\n\
[theme]\n\
base='light'\n\
primaryColor='#F63366'\n\
backgroundColor='#FFFFFF'\n\
secondaryBackgroundColor='#F0F2F6'\n\
textColor='#262730'\n\
" > ~/.streamlit/config.toml
