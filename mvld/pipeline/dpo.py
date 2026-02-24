from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import DPOTrainer
from datasets import Dataset
from typing import Optional
import torch

class MVLDDPOTrainer:
    """
    Direct Preference Optimization (DPO) Trainer for Manim code.
    Uses (prompt, chosen, rejected) triplets to reduce visual logic drift.
    """
    def __init__(self, model_id: str = "gpt2"): # Placeholder base model
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_id)
        self.ref_model = AutoModelForCausalLM.from_pretrained(model_id) # Usually same as model initially

    def train(self, dataset: Dataset, output_dir: str = "results/dpo"):
        """
        Runs DPO training.
        Dataset expected to have columns: [prompt, chosen, rejected]
        """
        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=2,
            num_train_epochs=3,
            logging_steps=10,
            learning_rate=1e-5,
            beta=0.1, # DPO temperature
            report_to="none"
        )

        dpo_trainer = DPOTrainer(
            self.model,
            self.ref_model,
            args=training_args,
            beta=0.1,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            max_length=512,
            max_prompt_length=256,
        )

        print(f"Starting DPO training on {len(dataset)} triplets...")
        # dpo_trainer.train() # Uncomment for actual training
        return dpo_trainer

if __name__ == "__main__":
    # Mockup dataset for testing initialization
    data = Dataset.from_list([
        {
            "prompt": "Draw a blue circle on the left.",
            "chosen": "circle.shift(LEFT).set_color(BLUE)",
            "rejected": "circle.shift(RIGHT).set_color(BLUE)"
        }
    ])
    
    trainer = MVLDDPOTrainer()
    print("DPO Trainer initialized.")
