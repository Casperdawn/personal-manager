#!/bin/bash

echo "开始打包 Personal Manager..."

PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
DIST_DIR="$PROJECT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

echo "1. 构建前端..."
cd "$FRONTEND_DIR"
npm run build --silent
if [ $? -ne 0 ]; then
    echo "前端构建失败！"
    exit 1
fi

echo "2. 准备静态文件..."
rm -rf "$BACKEND_DIR/static"
mkdir -p "$BACKEND_DIR/static"
cp -r "$FRONTEND_DIR/dist/"* "$BACKEND_DIR/static/"

echo "3. 生成示例数据..."
cd "$BACKEND_DIR"
source venv/bin/activate
rm -f personal_manager.db
python init_sample_data.py

echo "4. 打包后端..."
cd "$BACKEND_DIR"
pyinstaller \
    --distpath "$DIST_DIR" \
    --workpath "$BACKEND_DIR/build" \
    PersonalManager.spec

if [ $? -ne 0 ]; then
    echo "后端打包失败！"
    exit 1
fi

echo "5. 清理临时文件..."
rm -rf "$BACKEND_DIR/build"

echo "6. 复制可执行文件..."
cp "$DIST_DIR/PersonalManager" "$PROJECT_DIR/PersonalManager"

echo "7. 复制数据库..."
cp "$BACKEND_DIR/personal_manager.db" "$PROJECT_DIR/personal_manager.db"

echo ""
echo "✅ 打包完成！"
echo ""
echo "可执行文件位置: $PROJECT_DIR/PersonalManager"
echo "数据库文件位置: $PROJECT_DIR/personal_manager.db"
echo ""
echo "运行方式:"
echo "  ./PersonalManager"
echo ""
echo "然后在浏览器中访问: http://localhost:8000"
echo ""
echo "默认账号:"
echo "  用户名: hzs"
echo "  密码: 123"
