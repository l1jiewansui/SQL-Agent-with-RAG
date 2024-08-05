### 服务器信息

10.130.11.22

端口：10022

账号：gis2024

密码：gis2024

### conda

之后每次登录使用conda环境之前均需要执行如下命令。

source activate

每次退出conda环境都需要执行如下命令。

conda deactivate



### 登录与传输

ssh myh@10.79.231.87 -p 10022

scp -P 10022 C:\Users\lenovo\Desktop\llm2app\run_rag.py myh@10.79.231.87:/home/myh/myh

scp -P 10022 myh@10.79.231.87:/home/myh/myh/run_rag.py C:\Users\lenovo\Desktop\llm2app\

ssh -L 50000:localhost:50000 myh@10.79.231.87 -p 10022

ssh -L 8888:localhost:8888 myh@10.79.231.87 -p 10022

ssh -L 7860:localhost:7860 myh@10.79.231.87 -p 10022



### 查看存储

du -h /home/myh | sort -h



### DB-GPT API调用

curl -X POST "http://localhost:5670/api/v2/chat/completions" \
    -H "Authorization: Bearer $DBGPT_API_KEY" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{\"messages\":\"show space datas limit 5\",\"model\":\"glm-4-9b-chat\", \"chat_mode\": \"chat_data\", \"chat_param\": \"shengting\"}"



### 公开端口

sudo iptables -t nat -A PREROUTING -p tcp --dport 7860 -j REDIRECT --to-port 7860

server_name="0.0.0.0", server_port=7860



wandb api key 6c63e1173a6da006fa9a33f1bc4c741793a9d1a2



A8000

批处理大小 1 梯度累积步数16 124h 显卡占用10G

​                  4                      4  231h 显卡占用15G

fp16           1                      16 35h显卡占用10G

fp16           16                    1   37h             45G



4060ti

fp16           1                    16  63h             10G



4070     bf                                  41h              10G

​             fp                                  43                10G

4090     bf                                  18h              10G

​             fp                                  18h              10G

​                                                   19h



git clone https://www.modelscope.cn/Kwai-Kolors/Kolors



huggingfacetoken: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
