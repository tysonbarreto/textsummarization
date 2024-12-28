import transformers
from transformers import pipeline
from datasets import load_dataset




class ProcessData:
  
    def __init__(self, tokenizer, max_input, max_target):
        self.tokenizer = tokenizer
        self.max_input = max_input
        self.max_target = max_target

    def process_chat_summarization_data(self, data_to_process):
        #get the dialogue text
        inputs = [dialogue for dialogue in data_to_process['dialogue']]
        #tokenize text
        model_inputs = self.tokenizer(inputs,  max_length=self.max_input, padding='max_length', truncation=True)

        #tokenize labels
        with self.tokenizer.as_target_tokenizer():
            targets = self.tokenizer(data_to_process['summary'], max_length=self.max_target, padding='max_length', truncation=True)

        model_inputs['labels'] = targets['input_ids']
        #reuturns input_ids, attention_masks, labels
        return model_inputs
    

if __name__=="__main__":
    __all__=["ProcessData"]