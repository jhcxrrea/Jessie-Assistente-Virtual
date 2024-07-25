# **Assistente Virtual Jessie**

## **Apoio de Inteligência Artificial**

A Jessie é um assistente virtual avançado desenvolvido para facilitar tarefas diárias e fornecer respostas precisas. Utilizamos tecnologias de ponta para criar uma experiência interativa e eficiente.

## **Tecnologias Utilizadas**

- **Flask**: Utilizado para criar a API que gerencia as comunicações entre o frontend e o backend do assistente.
- **TensorFlow**: Empregado no desenvolvimento do modelo de reconhecimento de voz para melhorar a precisão na interpretação de comandos falados.
- **OpenCV**: Usado para o processamento de vídeo e reconhecimento de imagens, permitindo a análise visual das entradas.
- **NLTK**: Facilita o processamento de linguagem natural, essencial para a compreensão e manipulação de texto.
- **Spacy**: Utilizado para análise de sentimento e reconhecimento de entidades, ajudando a entender o contexto e a intenção dos comandos.
- **gTTS**: Converte texto em áudio, permitindo que o assistente responda de forma audível.
- **pyttsx3**: Utilizado como fallback para síntese de voz quando o gTTS não está disponível.
- **Tkinter**: Responsável pela criação da interface gráfica do usuário (GUI), proporcionando uma experiência visual amigável.
- **ScrolledText**: Permite a criação de áreas de texto roláveis na GUI para exibir o histórico de conversas e comandos.
- **Pandas**: Utilizado para a manipulação de dados, facilitando a gestão e análise de informações.
- **SymPy**: Usado para cálculos matemáticos e simplificação de expressões.

## **Instalação**
1. Clone esse repositório:
    ```bash
    git clone https://github.com/jhcxrrea/jessie
    ```
2. Instale as dependências listadas no `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure a chave de API da Hugging Face:
   - Crie um arquivo chamado `.env` no diretório do projeto.
   - Adicione sua chave de API da Hugging Face ao arquivo `.env` da seguinte forma:
     ```
     email=seu_email_da_hugingface_aqui
     pass=sua_senha_da_hugingface_aqui
     ```

## **Como Usar**
1. Baixe o arquivo `jessie.py` e execute-o utilizando um interpretador de Python.
2. Abra o aplicativo e inicie uma conversa com o assistente Jessie.
3. Utilize os comandos fornecidos para interagir com o assistente, que pode ajudar com tarefas diversas, como conversão de unidades e busca de informações.

## **Comandos**

- **desligar**: Encerra o aplicativo.
- **adeus**: Encerra o assistente.
- **hora**: Informa a hora atual.
- **data**: Informa a data atual.
- **quem é você**: Fala sobre o assistente.
- **abrir youtube**: Abre o YouTube.
- **abrir spotify**: Abre o Spotify.
- **tocar música**: Toca uma música.
- **previsão do tempo**: Fornece a previsão do tempo.
- **reproduzir música**: Reproduz uma música.
- **reproduzir vídeo**: Reproduz um vídeo.
- **abrir google**: Abre o Google.
- **abrir amazon**: Abre o Amazon.
- **pesquisar**: Procura informações na internet.
- **notícias**: Abre as notícias.
- **clima**: Fala sobre o clima.
- **definir lembrete**: Define um lembrete.
- **calcular**: Realiza cálculos matemáticos.
- **cotação do dólar**: Informa a cotação do dólar.
- **hora mundial**: Informa a hora em diferentes cidades.
- **criar nota**: Cria uma nota.
- **converter**: Converte unidades.

## **Desenvolvimento**

O assistente Jessie é desenvolvido com a colaboração de alunos e professores, visando criar uma ferramenta que melhore a vida das pessoas. O código inclui funcionalidades avançadas como reconhecimento de voz, conversão de texto para fala, processamento de linguagem natural, e uma interface gráfica moderna.

## **Detalhes Técnicos**

- **Reconhecimento de Voz**: O assistente usa a biblioteca `speech_recognition` para ouvir e transcrever comandos falados.
- **Síntese de Voz**: Utiliza `gTTS` e `pyttsx3` para converter texto em fala, garantindo uma resposta audível.
- **Processamento de Comandos**: Comandos são processados e executados, incluindo a busca em sites, reprodução de mídias e cálculos matemáticos.
- **Interface Gráfica**: Desenvolvida com `Tkinter`, inclui áreas de texto roláveis para histórico e visualização de comandos, com atualização em tempo real.
- **Funções Adicionais**: Incluem acesso a APIs para informações como clima, hora mundial e cotações financeiras.

## **Instruções para Contribuição**

Se você deseja contribuir para o projeto, por favor, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção.
3. Faça as alterações e envie um pull request.

## **Licença**

Este projeto é licenciado sob a [MIT License](LICENSE).

## **Contato**

Para dúvidas ou suporte, entre em contato com [jhcxrrea@gmail.com].
