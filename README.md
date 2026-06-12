# removebg-vercell

這是一個 Vercel Python Serverless Function，用 `transparent-background` 做圖片去背景 API。

## 使用方式

1. `POST /api/remove`，Request body 必須包含：
   ```json
   { "image_base64": "..." }
