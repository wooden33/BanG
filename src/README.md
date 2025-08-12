# Panta

### Environment setup
Create the environment using the following command:
```
conda create --name panta-env python=3.11
conda activate panta-env
```

Execute the following command to the project related dependencies:
```
poetry install
```

Please update the `panta-env.yml` file with the latest dependencies, if you have added or modified any new dependencies. 

##### Export the dependencies to a file
```
conda env export --no-builds | grep -v "^prefix: " > panta-env.yml
```

##### Chosing models
We support various LLMs. The full list of supported models is provided below:
- gpt-4o
- gpt-4o-mini
- llama3-3
- llama3-1
- claude3-5
- mistral-large

Choose your targeted _llm model_, _src file_, etc. The configrations can be filled in ```config.ini```

### Running the application
We use AWS Bedrock for open-source models (llama and mistral), you will need to set up your own aws credentials.

For proprietary models, you need to have your own API Key ready.

Using OPENAI models as an example, to run Panta,  execute the following command:

```
export OPENAI_API_KEY='OPENAI_API_KEY'
cd src/
python main.py
```

