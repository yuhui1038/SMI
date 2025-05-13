import os
import zstandard


def uncompress_zst_files(source_dir, target_dir):
    # 若目标目录不存在，则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历源目录下的所有文件
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.jsonl.zst'):
                file_path = os.path.join(root, file)
                # 构建解压后的文件名，去掉.zst后缀
                output_file_name = os.path.splitext(file)[0]
                output_file_path = os.path.join(target_dir, output_file_name)

                try:
                    # 打开压缩文件
                    with open(file_path, 'rb') as compressed_file:
                        dctx = zstandard.ZstdDecompressor()
                        with open(output_file_path, 'wb') as output_file:
                            # 解压文件
                            dctx.copy_stream(compressed_file, output_file)
                    print(f"已成功解压: {file_path} 到 {output_file_path}")
                except Exception as e:
                    print(f"解压 {file_path} 时出错: {e}")


if __name__ == "__main__":
    source_dir = 'datasets/pile-uncopyrighted/train'
    target_dir = 'datasets/pile_data'
    uncompress_zst_files(source_dir, target_dir)
    