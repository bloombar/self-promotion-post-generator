import os, random, requests
from datetime import datetime
from dotenv import load_dotenv
import openai
from PIL import Image, ImageFont, ImageDraw

load_dotenv()

def openai_connect():
  '''
  Connects to OpenAI API using the key in the .env file
  '''
  openai.api_key = os.getenv("OPENAI_API_KEY")
  print(f'Using API key: {openai.api_key}')
  # models = openai.Model.list()

def random_choice(the_list):
  '''
  Returns a random value from a list
  @param the_list: a list of values
  '''
  value = the_list[random.randint(0, len(the_list) - 1)]
  return value

# prompt settings
adjective_pool = ['social', 'cloud', 'community', 'naturopathic', 'diverse', 'integrative', 'machine', 'clean', 'data', 'education', 'academic', 'experience', 'software', 'data', 'plant-based', 'mycological', 'sustainable', 'green', 'ethical', "electric", 'product', 'user experience', 'innovation', 'computer-assisted', 'equity']
topic_pool = ["learning", "science", 'STEM', "automation", "innovation", "design", 'thinking', "development", "technology", 'programming', 'introspection', "privacy", 'AI', 'mining', 'insights', 'unicycling', 'design', 'innovation', 'entrepreneurship', 'fabrication', 'power']
action_pool = ['shipping', 'listening', 'proud of', 'honored to be part of', 'being humbled by', 'judging', 'donating', 'joining the team', 'starting a new position', 'speaking', 'organizing', 'presenting', 'sharing', 'orchestrating', 'winning', 'awarding', 'selecting', 'receiving']
utterance_type_pool = ['announcing', 'saying how proud i am of', 'telling you about', 'sharing', 'helping you to understand', 'not too proud to say']
event_pool = ['product launch', 'IPO', 'conference', 'workshop', 'talk', 'webinar', 'keynote', 'seminar', 'class', 'course', 'training', 'workshop', 'award', 'grant', 'scholarship', 'fellowship', 'competition', 'hackathon']
people_pool = ["business people", "yoga gurus", "young adults in tee shirts", "diverse children", "a beautiful woman", "academics", "women over 50", "middle-aged men"]
object_pool = ["computer", "phone", "futuristic device", "electric unicycle", "loom", 'drone', 'flower', 'gear', 'supernatural power', 'cloud', 'antique tv', 'fjord', 'old wooden house', 'hammer', 'sickle', 'sun']
image_type_pool = ['photo', 'drawing', 'painting', 'sketch', 'illustration', 'infographic', 'chart']
image_style_pool = ['brutalist', 'black-and-white', 'landscape', 'futuristic', 'modernist', 'greek', 'surreal', 'pop art', 'photorealistic', 'cubist']

def random_prompt():
  # randomize prompt settings
  prompt = {
    "topic": f'{random_choice(adjective_pool)} {random_choice(topic_pool)}',
    "action": random_choice(action_pool),
    'utterance_type': random_choice(utterance_type_pool),
    "event_type": random_choice(event_pool),
    "people": random_choice(people_pool),
    "object": random_choice(object_pool),
    "image_style": random_choice(image_style_pool),
    "image_type": random_choice(image_type_pool)
  }

  # generate prompt texts
  prompt["event"] = f'{prompt["action"]} at a {prompt["topic"]} {prompt["event_type"]}'
  prompt["text_prompt"] = f'Write a one sentence, informal first person message {prompt["utterance_type"]} my {prompt["event"]}.  Give the event a fake name, and optionally a specific location and a random date within a few weeks after {datetime.now()}.'
  prompt["image_prompt"] = f'Create a simple {prompt["image_style"]} {prompt["image_type"]}, with {prompt["people"]} and a(n) {prompt["object"]}.'

  return prompt

def package_message(role, content):
  '''
  Returns a message object for OpenAI API
  @param role: 'user', 'system', or 'assistant'
  @param content: the message content to send to the bot
  '''
  message = {
    "role": role,
    "content": content
  }
  return message

def get_response(messages):
  '''
  Returns a response from OpenAI API, given the inputes in 'messages'
  '''
  response = openai.ChatCompletion.create(
      model=os.getenv("OPENAI_MODEL"),
      messages=messages,
      temperature=0.8,
  )
  messages.append(package_message('assistant', response['choices'][0]['message']['content']))
  response_text = response['choices'][0]['message']['content']
  return response_text

def main():
  # seed with initial message with system instructions
  messages = [
    package_message('system', "You are a helpful assistant that is helping to write promotional materials for an individual and a team."),
    package_message('user', 'Write a one sentence, informal first person message explaining my sharing at a education design award.  Give the event a fake name, and optionally a specific location and a random date within a few weeks after 2023-03-24 23:06:15.925451.'),
    package_message('assistant', "Excited to share that I'll be presenting at the upcoming InnovateEd Conference in New York City on April 14th about our award-winning education design project.  Hope to see some of you there!"),
    package_message('user', 'Write a one sentence, informal first person message announcing my professing at a software power class.  Give the event a fake name, and optionally a specific location and a random date within a few weeks after 2023-03-24 23:10:01.481857.'),
    package_message('assistant', "Just wanted to let you know that I'll be speaking at the CodeCon West conference in San Francisco on May 5th, where I'll be sharing some tips and tricks for building powerful software!  Should be a great event."),
  ]

  # generate prompt
  prompt = random_prompt()
  messages.append(package_message('user', prompt['text_prompt'])) # attach the text prompt to the inputs

  # generate text
  promotion_text = get_response(messages)

  # generate some random hash tags
  messages.append(package_message('user', "Generate between 1 and 4 random hash tags to go along with this."))
  hash_tags = get_response(messages)
  promotion_text += ' ' + hash_tags

  # generate an organization name
  messages.append(package_message('user', f'Generate a random organization name for this {prompt["event_type"]}.'))
  organization_name = get_response(messages)
  print(f'Organization name: {organization_name}') 

  # generate corresponding poster
  response = openai.Image.create(
    prompt=prompt['image_prompt'],
    n=1,
    size="1024x1024"
  )

  # timestamp for saving files
  timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
  posts_dir = os.path.join(os.getcwd(), "posts") # save into `images` subdirectory

  # save the response text to file
  response_text_name = f'{timestamp}-post.txt'  # any name you like; the filetype should be .txt
  response_text_filepath = os.path.join(posts_dir, response_text_name)
  with open(response_text_filepath, "w") as text_file:
      text_file.write(promotion_text)  # write the text to the file

  # save generated image to file
  image_url = response['data'][0]['url']
  generated_image_name = f'{timestamp}-image.png'  # any name you like; the filetype should be .png
  generated_image_filepath = os.path.join(posts_dir, generated_image_name)
  generated_image_url = response["data"][0]["url"]  # extract image URL from response
  generated_image = requests.get(generated_image_url).content  # download the image
  with open(generated_image_filepath, "wb") as image_file:
      image_file.write(generated_image)  # write the image to the file

  # output
  print(f'Prompt text: {prompt["text_prompt"]}')
  print(promotion_text)
  print(f'Image prompt: {prompt["image_prompt"]}')
  print(f'Image file: {generated_image_filepath}')


# execute if running directly
if __name__ == "__main__":
  openai_connect()
  main()
