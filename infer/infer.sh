
# # 101
# CUDA_VISIBLE_DEVICES=4 python infer/infer.py --total_part 5 --part_id 0 &
# CUDA_VISIBLE_DEVICES=3 python infer/infer.py --total_part 5 --part_id 1 &

# # 102
# CUDA_VISIBLE_DEVICES=2 python infer/infer.py --total_part 5 --part_id 2 &

# # 47
# CUDA_VISIBLE_DEVICES=1 python infer/infer.py --total_part 5 --part_id 3 &
# CUDA_VISIBLE_DEVICES=0 python infer/infer.py --total_part 5 --part_id 4 &

# new 47
CUDA_VISIBLE_DEVICES=7 python infer/infer_vllm.py --total_part 4 --part_id 0 &
CUDA_VISIBLE_DEVICES=0 python infer/infer_vllm.py --total_part 4 --part_id 1 &
CUDA_VISIBLE_DEVICES=7 python infer/infer_vllm.py --total_part 4 --part_id 2 &
CUDA_VISIBLE_DEVICES=7 python infer/infer_vllm.py --total_part 4 --part_id 3 &
