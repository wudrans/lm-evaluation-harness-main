
# lm_eval --model hf \
#    --model_args pretrained=/data/wlj/pretrained/Qwen/Qwen3-0.6B \
#    --tasks hellaswag \
#    --device cuda:0 \
#    --batch_size 8



# lm_eval --model vllm \
#    --model_args pretrained=/data/wlj/pretrained/Qwen/Qwen3-0.6B \
#    --tasks hellaswag \
#    --device cuda:0 \
#    --batch_size 8



lm_eval --model vllm \
   --model_args pretrained=/data/wlj/pretrained/Qwen_quantize-awq-sym/Qwen3-0.6B \
   --tasks hellaswag \
   --device cuda:0 \
   --batch_size 8