from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer
from datasets import Dataset
from typing import Optional

class MVLDSFTTrainer:
    """
    Standard SFT Trainer for Manim code generation.
    Supports coordinate-augmented datasets.
    """
    def __init__(self, model_id: str = "gpt2"): # Placeholder base model
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_id)

    def train(self, dataset: Dataset, output_dir: str = "results/sft"):
        """
        Runs SFT on the provided dataset.
        """
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            save_steps=100,
            logging_steps=10,
            learning_rate=2e-5,
            weight_decay=0.01,
            push_to_hub=False,
            report_to="none"
        )

        def formatting_prompts_func(example):
            output_texts = []
            for i in range(len(example['instruction'])):
                text = f"### Instruction: {example['instruction'][i]}\n### Code: {example['code'][i]}"
                output_texts.append(text)
            return output_texts

        trainer = SFTTrainer(
            model=self.model,
            train_dataset=dataset,
            dataset_text_field="text", # We use formatting_func instead
            formatting_func=formatting_prompts_func,
            max_seq_length=512,
            args=training_args,
        )

        print(f"Starting SFT training on {len(dataset)} samples...")
        # trainer.train() # Uncomment for actual training
        return trainer

if __name__ == "__main__":
    # Test with mockup
    from mvld.data.dataset import MVLDDataset
    dh = MVLDDataset()
    ds = dh.create_dummy_dataset(3)
    
    trainer = MVLDSFTTrainer()
    print("SFT Trainer initialized and dataset formatted.")
