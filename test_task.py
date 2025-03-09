from dotenv import load_dotenv
load_dotenv()


from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
import os
import json
from pydantic import SecretStr
from browser_use import Agent, Controller


ds_api_key = os.getenv("DEEPSEEK_API_KEY")
ds = ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-reasoner', api_key=SecretStr(ds_api_key))


gpt_api_key = os.getenv("OPENAI_API_KEY")
gpt = ChatOpenAI(base_url='https://api.chatanywhere.tech', model='gpt-4o-mini', api_key=SecretStr(gpt_api_key))

controller = Controller()

@controller.action(
	'Save text to txt file.',
)
async def save_text(text: str, path: str = './output.txt'):
	with open(path, 'a') as fp:
		fp.write(text)

# @controller.action(
# 	'Load account and password from my config json file.',
# )
# async def load_account_password():
# 	with open('./config.json', 'r') as fp:
# 		config = json.load(fp)
# 		return config


# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        chrome_instance_path="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

# Create the agent with your configured browser
agent = Agent(
    task="Go to google, search for good projects and papers that help students to learn reinforcement learning. Go to google docs, log in my account, create a new doc, save the projects and papers in it. Ask me for help if necessary",
    llm=ds,
    browser=browser,
    controller=controller,
)

async def main():
    await agent.run()

    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())