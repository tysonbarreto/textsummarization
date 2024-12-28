from src.textsummarization.utils import read_yaml, activate_root_directory
from src.textsummarization.logger import Logger
from src.textsummarization.exception import TSException
from src.textsummarization.process_data import ProcessData

import transformers
from transformers import pipeline
from datasets import load_dataset
import torch
import evaluate
import numpy as np
import nltk
from box import ConfigBox
nltk.download('punkt')

import os, sys

logger = Logger()

def chat_summarizer_run() -> None:
    try:
        logger.info("<<<< Chat Summarization Trainer is being initialized... >>>>")
        config = read_yaml('config.yml', return_configbox=True)
        chat_sum_config = config.chat_summarization
        logger.info("==== Config file successfully loaded ====")

        logger.info("==== Dependencies imported successfully ====")

        data = load_dataset(chat_sum_config.dataset)
        metric = evaluate.load(chat_sum_config.metric)
        model_checkpoints = chat_sum_config.model_checkpoints

        logger.info(f"==== Loaded ====\n- dataset\n- metric\n- model_checkpoint\n")

        max_input = chat_sum_config.max_input
        max_target = chat_sum_config.max_target
        tokenizer = transformers.AutoTokenizer.from_pretrained(model_checkpoints)

        logger.info("==== Tokenizer configured ====")

        process_data = ProcessData(tokenizer=tokenizer, max_input= max_input, max_target=max_target)

        tokenize_data = data.map(process_data.process_chat_summarization_data, batched = True, remove_columns=['id', 'dialogue', 'summary'])

        logger.info("==== Dataset Tokenized ====")

        train_sample = tokenize_data['train'].shuffle(seed=42).select(range(5000))
        validation_sample = tokenize_data['validation'].shuffle(seed=42).select(range(250))
        test_sample = tokenize_data['test'].shuffle(seed=42).select(range(100))

        tokenize_data['train'] = train_sample
        tokenize_data['validation'] = validation_sample
        tokenize_data['test'] = test_sample

        model = transformers.AutoModelForSeq2SeqLM.from_pretrained(model_checkpoints)

        collator = transformers.DataCollatorForSeq2Seq(tokenizer, model=model)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        logger.info(f"==== {device} found! ====")

        args = transformers.Seq2SeqTrainingArguments(
        'artifacts/chat_summarization/conversation-summ',
        eval_strategy='epoch',
        learning_rate=float(chat_sum_config.learning_rate),
        per_device_train_batch_size=1,
        per_device_eval_batch_size= 1,
        gradient_accumulation_steps=2,
        weight_decay=float(chat_sum_config.weight_decay),
        save_total_limit=2,
        num_train_epochs=3,
        predict_with_generate=True,
        eval_accumulation_steps=1,
        report_to='none',
        fp16= False if device.type=='cpu' else True,
        )

        trainer = transformers.Seq2SeqTrainer(
        model,
        args,
        train_dataset=tokenize_data['train'],
        eval_dataset=tokenize_data['validation'],
        data_collator=collator,
        processing_class=tokenizer
        )   

        logger.info("==== Model, DataCollator, TrainingArgs and Trainer configured successfully ====")

        logger.info("==== Intializing Training.... ====")

        trainer.train()

        logger.info("==== Training Completed! ====")

        trainer.save_model('artifacts/chat_summarization/chat_summarization_pretrained_model')
        tokenizer.save_pretrained("artifacts/chat_summarization/chat_summarization_tokenizer")
        logger.info("Fine-Tuned chat summarization model and tokenizer is saved in artifacts/chat_summarization directory")

    except Exception as e:
        logger.error(TSException(e,sys))
        raise TSException(e,sys)
    
if __name__ == "__main__":
    torch.multiprocessing.freeze_support()
    chat_summarizer_run()