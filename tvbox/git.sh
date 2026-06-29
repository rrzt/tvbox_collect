#!/usr/bin/env bash
# ====================================================
# 项目名称: Git Master 终端可视化管理脚本 (完整重构版 v2)
# 运行环境: 适配 Android / Termux / MT 管理器终端环境
# 核心原则: 独立执行单步操作，采用现代 Git 命令，详细注释
# 新增模块: 初始化向导 / 暂存管理 / 撤销操作 / 身份配置 / 克隆仓库
# ====================================================

# ================= 配置区 =================
# 专属 Github 仓库地址与日志绝对路径 (请勿随意修改)
MY_REPO_URL="https://github.com/cluntop/tvbox.git"
LOG_FILE="/storage/emulated/0/box/.github/git.log"
LOG_DIR=$(dirname "$LOG_FILE")   # FIX: 全局缓存，避免每次调用 dirname

# ================= 颜色与样式 =================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # 恢复默认配色

# ================= 基础核心函数 =================

# 初始化日志目录 (单独执行，避免与其他命令合并)
init_log_dir() {
    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR" 2>/dev/null
    fi
}
init_log_dir

# 统一日志记录器
log() {
    if [ -w "$LOG_DIR" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    fi
}

# FIX: 消息函数现在实际使用颜色变量（原版定义了颜色但从未使用）
success_msg() { echo -e "${GREEN}✔ $1${NC}"; log "成功: $1"; }
error_msg()   { echo -e "${RED}✘ $1${NC}"; log "错误: $1"; }
warn_msg()    { echo -e "${YELLOW}⚠ $1${NC}"; log "警告: $1"; }
info_msg()    { echo -e "${CYAN}ℹ $1${NC}"; }
title_msg()   { echo -e "\n${BOLD}${PURPLE}>>> $1 <<<${NC}\n"; }

# 依赖检查：验证 Git 是否已安装
check_git() {
    # command -v 是检测命令是否存在的标准 POSIX 写法
    if ! command -v git > /dev/null 2>&1; then
        error_msg "致命错误: 未检测到 Git 环境，请先安装 Git。"
        exit 1
    fi
}

# 环境检查：验证当前是否处于 Git 仓库工作区内 (支持子目录识别)
check_git_repo() {
    # 现代标准写法：无论在仓库的哪个子目录，只要受 git 管理都会返回 true
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 安全的分页输出：优先使用 less，降级为直接打印
paged_output() {
    if command -v less > /dev/null 2>&1; then
        less -R
    else
        cat
    fi
}

# ================= 业务功能模块 =================

# 1. 暂存变动 (Git Add)
do_add() {
    title_msg "📝 步骤 1/3: 暂存文件 (Git Add)"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库，请先初始化"
        return 1
    fi

    # 获取工作区变动情况
    local changes
    changes=$(git status --porcelain)
    if [ -z "$changes" ]; then
        warn_msg "工作区纯净，没有需要暂存的修改文件。"
        return 0
    fi

    echo -e "待暂存的变更文件:"
    git status --short
    echo ""

    info_msg "正在执行文件追踪 (git add .) ..."
    if git add .; then
        success_msg "所有变更已成功加入暂存区！"
        return 0
    else
        error_msg "暂存失败，请检查文件权限。"
        return 1
    fi
}

# 2. 创建快照 (Git Commit)
do_commit() {
    title_msg "📦 步骤 2/3: 提交快照 (Git Commit)"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库，请先初始化"
        return 1
    fi

    # 检查暂存区是否有待提交的内容
    local staged_changes
    staged_changes=$(git diff --cached --name-only)
    if [ -z "$staged_changes" ]; then
        warn_msg "暂存区为空。请先执行 [1] 暂存文件 (Add) 再进行提交。"
        return 0
    fi

    # 捕获用户自定义提交信息
    read -p "请输入提交信息 (直接回车默认: Update Up): " msg
    if [ -z "$msg" ]; then
        msg="Update Up"
    fi

    info_msg "正在生成本地提交快照..."
    if git commit -m "$msg"; then
        success_msg "版本快照生成完毕！"
        return 0
    else
        error_msg "提交失败，请检查配置或终端输出。"
        return 1
    fi
}

# 3. 单独执行：推送云端 (Git Push)
do_push() {
    title_msg "🚀 步骤 3/3: 推送至云端 (Git Push)"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi

    # 获取当前所在分支 (现代命令 --show-current)
    local curr
    curr=$(git branch --show-current)
    if [ -z "$curr" ]; then curr="main"; fi

    info_msg "正在推送数据包至 origin/$curr ..."
    if git push origin "$curr"; then
        success_msg "代码已成功同步至云端！"
        return 0
    else
        warn_msg "常规推送被拒绝。远程仓库可能包含您本地没有的更改。"
        read -p "⚠ 是否执行安全强制推送 (--force-with-lease)? (y/n): " force_push
        if [[ "$force_push" =~ ^[Yy]$ ]]; then
            info_msg "启动安全覆盖协议 (git push --force-with-lease) ..."
            if git push --force-with-lease --set-upstream origin "$curr"; then
                success_msg "安全强推成功！远程状态已被本地更新覆盖。"
                return 0
            else
                error_msg "强推失败，可能存在更严重的冲突或网络问题。"
                return 1
            fi
        else
            info_msg "操作已取消。建议先执行拉取操作。"
            return 1
        fi
    fi
}

# 4. 拉取更新 (Git Pull)
# FIX: stash 后自动执行 pop，不再只打印提示让用户手动处理
do_pull() {
    title_msg "📥 拉取最新更新 (Git Pull)"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi

    local curr
    curr=$(git branch --show-current)
    if [ -z "$curr" ]; then curr="main"; fi

    info_msg "1/2 探测远程状态 (git fetch)..."
    git fetch origin 2>/dev/null

    # 冲突阻断机制
    local local_changes
    local_changes=$(git status --porcelain)
    local did_stash=false

    if [ -n "$local_changes" ]; then
        warn_msg "检测到本地有未提交的更改，直接拉取可能导致冲突！"
        read -p "是否先暂存 (stash) 本地更改，安全拉取后自动恢复? (y/n): " stash_choice
        if [[ "$stash_choice" =~ ^[Yy]$ ]]; then
            git stash push -m "auto-stash before pull $(date '+%H:%M:%S')"
            did_stash=true
            info_msg "本地更改已存入 stash。"
        fi
    fi

    info_msg "2/2 下载与合并 (git pull origin $curr)..."
    if git pull origin "$curr"; then
        success_msg "拉取成功，本地已是最新版本。"
        # FIX: 自动恢复 stash，不再只打印提示
        if [ "$did_stash" = true ]; then
            info_msg "正在自动恢复您之前暂存的代码 (git stash pop)..."
            if git stash pop; then
                success_msg "本地代码已自动恢复！"
            else
                warn_msg "自动恢复失败，可能存在合并冲突，请手动执行 git stash pop 并解决冲突。"
            fi
        fi
        return 0
    else
        error_msg "拉取过程产生冲突或网络连接失败。"
        if [ "$did_stash" = true ]; then
            warn_msg "注意：您有代码存于 stash，解决冲突后请手动执行 git stash pop。"
        fi
        return 1
    fi
}

# 5. 分支管理 (新增：删除分支)
manage_branches() {
    title_msg "🌿 分支管理 (Branch)"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi
    
    echo -e "当前分支列表:"
    git branch -a
    echo ""
    echo "1) 创建并切换至新分支"
    echo "2) 切换到已存在的分支"
    echo "3) 删除本地分支"
    echo "4) 返回主菜单"
    read -p "请选择分支指令编号: " b_choice
    
    case $b_choice in
        1)
            read -p "请输入新分支名称 (无空格): " b_name
            if [ -n "$b_name" ]; then
                if git switch -c "$b_name"; then
                    success_msg "已创建并切换至新分支: $b_name"
                    return 0
                else
                    error_msg "分支创建失败"
                    return 1
                fi
            else
                # FIX: 原来空名称时静默无提示，现在明确报错
                error_msg "分支名称不能为空"
                return 1
            fi
            ;;
        2)
            read -p "请输入目标分支名称: " b_name
            if [ -n "$b_name" ]; then
                if git switch "$b_name"; then
                    success_msg "成功切换至分支: $b_name"
                    return 0
                else
                    error_msg "分支切换失败"
                    return 1
                fi
            else
                # FIX: 原来空名称时静默无提示，现在明确报错
                error_msg "分支名称不能为空"
                return 1
            fi
            ;;
        3)
            read -p "请输入要删除的本地分支名称: " b_name
            if [ -n "$b_name" ]; then
                local curr
                curr=$(git branch --show-current)
                if [ "$b_name" = "$curr" ]; then
                    error_msg "无法删除当前所在分支，请先切换到其他分支。"
                    return 1
                fi
                read -p "⚠ 确认删除本地分支 '$b_name'? (y/n): " confirm
                if [[ "$confirm" =~ ^[Yy]$ ]]; then
                    if git branch -d "$b_name"; then
                        success_msg "分支 '$b_name' 已删除。"
                        return 0
                    else
                        warn_msg "该分支存在未合并的提交，是否强制删除?"
                        read -p "强制删除? (y/n): " force_del
                        if [[ "$force_del" =~ ^[Yy]$ ]]; then
                            if git branch -D "$b_name"; then
                                success_msg "已强制删除分支 '$b_name'。"
                                return 0
                            fi
                        fi
                    fi
                fi
            else
                error_msg "分支名称不能为空"
                return 1
            fi
            ;;
        4)
            info_msg "操作取消"
            return 0
            ;;
        *)
            error_msg "无效选项"
            return 1
            ;;
    esac
}

# 6. 状态明细
# FIX: diff 使用 less -R 分页，避免改动多时刷屏
view_status() {
    title_msg "📊 库区状态剖析"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi

    echo -e "${BOLD}【当前文件级状态概览 (git status -s)】${NC}"
    git status -s
    echo ""

    echo -e "${BOLD}【工作区尚未暂存的代码变动 (git diff)】${NC}"
    git --no-pager diff | paged_output
    echo ""

    echo -e "${BOLD}【已放入暂存区待提交的代码变动 (git diff --cached)】${NC}"
    git --no-pager diff --cached | paged_output
    echo ""
    return 0
}

# 7. 历史查询
view_logs() {
    title_msg "📜 提交历史溯源"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi
    git --no-pager log --graph \
        --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' \
        --abbrev-commit -n 15
    echo -e "\n"
    return 0
}

# 8. 绑定远程地址
bind_remote() {
    title_msg "🔗 绑定远程仓库地址"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi
    
    local current_url
    current_url=$(git remote get-url origin 2>/dev/null || echo "未绑定")

    echo -e "当前设备识别到的源地址: ${CYAN}$current_url${NC}"
    echo -e "脚本预设的目标源地址:   ${CYAN}$MY_REPO_URL${NC}"

    read -p "确认将本地仓库指向预设目标地址吗? (y/n): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        git remote remove origin 2>/dev/null
        if git remote add origin "$MY_REPO_URL"; then
            success_msg "远程源绑定成功！"
            return 0
        else
            error_msg "绑定失败，请检查权限。"
            return 1
        fi
    fi
    return 0
}

# 9. NEW: 初始化向导 (init + config + bind remote 三合一)
# FIX: 兼容旧版 Git (< 2.28)，不依赖 --initial-branch 参数
init_wizard() {
    title_msg "🧙 初始化向导 (Init Wizard)"
    if check_git_repo; then
        error_msg "阻止操作：当前已经是受控 Git 仓库"
        return 1
    fi

    # Step 1: git init
    info_msg "[1/3] 初始化 Git 仓库..."
    if git init; then
        # 兼容旧版 Git：通过 symbolic-ref 设置默认分支为 main
        git symbolic-ref HEAD refs/heads/main 2>/dev/null || true
        success_msg "仓库初始化完毕！默认分支已设为 main。"
    else
        error_msg "初始化失败"
        return 1
    fi

    # Step 2: 用户身份配置
    info_msg "[2/3] 配置 Git 身份信息..."
    local cur_name cur_email
    cur_name=$(git config --global user.name 2>/dev/null)
    cur_email=$(git config --global user.email 2>/dev/null)
    echo -e "当前 user.name  : ${CYAN}${cur_name:-未设置}${NC}"
    echo -e "当前 user.email : ${CYAN}${cur_email:-未设置}${NC}"

    read -p "请输入 user.name  (回车跳过): " new_name
    if [ -n "$new_name" ]; then
        git config --global user.name "$new_name"
        success_msg "user.name 已设为: $new_name"
    fi

    read -p "请输入 user.email (回车跳过): " new_email
    if [ -n "$new_email" ]; then
        git config --global user.email "$new_email"
        success_msg "user.email 已设为: $new_email"
    fi

    # Step 3: 绑定远程
    info_msg "[3/3] 绑定远程仓库..."
    echo -e "预设远程地址: ${CYAN}$MY_REPO_URL${NC}"
    read -p "是否绑定到此地址? (y/n): " bind_confirm
    if [[ "$bind_confirm" =~ ^[Yy]$ ]]; then
        git remote remove origin 2>/dev/null
        if git remote add origin "$MY_REPO_URL"; then
            success_msg "远程地址绑定成功！"
        else
            error_msg "远程地址绑定失败。"
        fi
    fi

    echo -e "【当前文件级状态概览 (git status -s)】"
    git status -s
    echo ""
    success_msg "🎉 初始化向导完成！可以开始使用 Add → Commit → Push 工作流了。"
    return 0
}

# 10. 切换目录
# FIX: 移除永远为真的 if 判断，cd 成功即确认
change_dir() {
    title_msg "📁 切换物理工作目录"
    echo -e "当前系统位置: $(pwd)"
    read -p "请输入新路径 (绝对/相对均可): " new_path
    if [ -n "$new_path" ]; then
        if [ ! -d "$new_path" ]; then
            mkdir -p "$new_path" 2>/dev/null
        fi
        if cd "$new_path"; then
            success_msg "系统位置已成功转移至: $(pwd)"
            return 0
        else
            error_msg "无法进入指定路径"
            return 1
        fi
    fi
    return 0
}

# 11. 深度清理
# FIX: 同时检查两条命令的执行结果
deep_clean() {
    title_msg "🧹 垃圾回收与深度清理"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi
    
    info_msg "清理历史动作残留并压缩数据库..."
    if git reflog expire --expire=now --all 2>/dev/null && \
       git gc --prune=now --aggressive 2>/dev/null; then
        success_msg "清理成功！当前 .git 体积为: $(du -sh .git 2>/dev/null | cut -f1)"
        return 0
    else
        error_msg "清理任务中断或失败。"
        return 1
    fi
}

# 12. NEW: 统一暂存管理 (Stash 子菜单，整合 Save / Pop / Drop)
manage_stash() {
    title_msg "📦 暂存管理 (Stash)"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi

    echo -e "${BOLD}【当前暂存记录列表】${NC}"
    local stash_count
    stash_count=$(git stash list | wc -l)
    
    if [ "$stash_count" -eq 0 ]; then
        echo -e "  (暂无记录)"
    else
        git --no-pager stash list
    fi
    echo ""
    echo "1) 🗃  存入暂存 (Stash Save) — 将工作区改动压入 stash"
    echo "2) 📤 恢复最新 (Stash Pop)  — 弹出最新一条并合并到工作区"
    echo "3) 🗑  删除记录 (Stash Drop) — 删除指定的 stash 条目"
    echo "4) 🔙 返回主菜单"
    read -p "请选择操作: " s_choice

    case $s_choice in
        1)
            local local_changes
            local_changes=$(git status --porcelain)
            if [ -z "$local_changes" ]; then
                warn_msg "工作区纯净，没有需要暂存的改动。"
                return 0
            fi
            read -p "请输入暂存备注 (回车使用默认): " stash_msg
            if [ -z "$stash_msg" ]; then
                stash_msg="manual-stash $(date '+%m-%d %H:%M')"
            fi
            if git stash push -m "$stash_msg"; then
                success_msg "当前改动已安全存入 stash: $stash_msg"
                return 0
            else
                error_msg "存入暂存失败。"
                return 1
            fi
            ;;
        2)
            if [ "$stash_count" -eq 0 ]; then
                warn_msg "当前没有任何暂存记录。"
                return 0
            fi
            local local_changes
            local_changes=$(git status --porcelain)
            if [ -n "$local_changes" ]; then
                warn_msg "高危拦截：工作区存在未提交的修改，此时释放 stash 可能产生冲突！"
                read -p "是否仍要尝试恢复? (y/n): " force_pop
                if [[ ! "$force_pop" =~ ^[Yy]$ ]]; then
                    info_msg "操作已安全取消。"
                    return 0
                fi
            fi
            info_msg "正在释放 stash (git stash pop)..."
            local pop_output pop_status
            pop_output=$(git stash pop 2>&1)
            pop_status=$?
            echo -e "$pop_output"
            if [ $pop_status -eq 0 ]; then
                success_msg "恢复成功！暂存代码已回到工作区。"
                return 0
            elif echo "$pop_output" | grep -q "Aborting"; then
                error_msg "恢复被 Git 中止！工作区存在冲突文件，请先提交或丢弃后再试。"
                return 1
            else
                error_msg "恢复产生合并冲突！请解决文件内的冲突标记 (<<<<<<<) 后手动提交。"
                return 1
            fi
            ;;
        3)
            if [ "$stash_count" -eq 0 ]; then
                warn_msg "当前没有任何暂存记录。"
                return 0
            fi
            echo ""
            git --no-pager stash list
            echo ""
            read -p "请输入要删除的编号 (如输入 0 代表 stash@{0}): " stash_idx
            if [[ "$stash_idx" =~ ^[0-9]+$ ]]; then
                read -p "⚠ 确认删除 stash@{$stash_idx}? 此操作不可恢复! (y/n): " del_confirm
                if [[ "$del_confirm" =~ ^[Yy]$ ]]; then
                    if git stash drop "stash@{$stash_idx}"; then
                        success_msg "已成功删除 stash@{$stash_idx}。"
                        return 0
                    else
                        error_msg "删除失败，请确认编号是否正确。"
                        return 1
                    fi
                fi
            else
                error_msg "请输入有效的数字编号。"
                return 1
            fi
            ;;
        4)
            info_msg "返回主菜单"
            return 0
            ;;
        *)
            error_msg "无效选项"
            return 1
            ;;
    esac
}

# 13. 一键同步 (完整修复版)
# FIX1: 修正执行顺序 → Stash(保护) → Pull → Pop → Add → Commit → Push
# FIX2: 提交信息附带时间戳，与原注释一致
do_one_click() {
    title_msg "⚡ 执行一键同步工作流"
    if ! check_git_repo; then 
        error_msg "当前目录非 Git 仓库"
        return 1
    fi

    local curr
    curr=$(git branch --show-current 2>/dev/null)
    if [ -z "$curr" ]; then curr="main"; fi

    local did_stash=false

    # Step 0: 检测本地改动，提前 stash 保护，再拉取
    local local_changes
    local_changes=$(git status --porcelain)
    if [ -n "$local_changes" ]; then
        info_msg "[0/5] 检测到本地改动，自动存入 stash 保护..."
        if git stash push -m "auto-stash $(date '+%m-%d %H:%M:%S')"; then
            did_stash=true
            success_msg "本地改动已安全暂存。"
        else
            error_msg "自动暂存失败，终止同步以保护您的代码。"
            return 1
        fi
    fi

    # Step 1: 拉取
    info_msg "[1/5] 正在拉取远程更新 (Git Pull)..."
    local pull_out
    # 捕获原生输出和错误
    pull_out=$(git pull origin "$curr" 2>&1)
    if [ $? -ne 0 ]; then
        error_msg "拉取失败！Git 报错："
        echo -e "$pull_out"
        [ "$did_stash" = true ] && warn_msg "您的代码已安全保存在 stash 中，请手动 git stash pop 恢复。"
        return 1
    fi

    # Step 2: 恢复 stash
    if [ "$did_stash" = true ]; then
        info_msg "[2/5] 正在恢复暂存代码 (Git Stash Pop)..."
        local pop_out
        pop_out=$(git stash pop 2>&1)
        if [ $? -ne 0 ]; then
            error_msg "恢复暂存失败！可能存在合并冲突，请手动解决。"
            echo -e "$pop_out"
            return 1
        fi
        success_msg "暂存代码已恢复。"
    else
        info_msg "[2/5] 无暂存记录，自动跳过。"
    fi

    # Step 3: Add
    info_msg "[3/5] 正在追踪变动文件 (Git Add)..."
    if ! git add . 2>&1; then
        error_msg "暂存文件失败！"
        return 1
    fi

    # 4. 提交快照 (Commit)
    info_msg "[4/5] 正在生成快照 (Git Commit)..."
    # 如果有可提交的改动才执行 commit
    if ! git diff --cached --quiet; then
        local commit_msg="Update Up"
        if ! git commit -m "$commit_msg"; then
            error_msg "提交代码失败！"
            return 1
        fi
    else
        warn_msg "工作区没有新变动，跳过提交。"
    fi

    # Step 5: Push
    info_msg "[5/5] 正在推送至云端 (Git Push)..."
    local push_out
    push_out=$(git push origin "$curr" 2>&1)
    if [ $? -ne 0 ]; then
        error_msg "推送失败！Git 报错："
        echo -e "$push_out"
        return 1
    fi

    success_msg "🎉 一键同步工作流全部执行成功！"
    return 0
}

# 14. NEW: 撤销操作 (Undo/Reset/Restore)
undo_changes() {
    title_msg "↩️  撤销操作 (Undo)"
    if ! check_git_repo; then
        error_msg "当前目录非 Git 仓库"
        return 1
    fi

    echo "1) 撤销最近一次 commit，改动退回暂存区  — git reset HEAD~1 --soft"
    echo "2) 撤销最近一次 commit，改动退回工作区  — git reset HEAD~1 --mixed"
    echo "3) 丢弃工作区全部未暂存改动             — git restore ."
    echo "4) 丢弃指定文件的未暂存改动             — git restore <file>"
    echo "5) 将指定文件移出暂存区 (取消 git add)  — git restore --staged <file>"
    echo "6) 返回主菜单"
    echo ""
    read -p "请选择操作: " u_choice

    case $u_choice in
        1)
            warn_msg "将撤销最近一次 commit，改动退回暂存区 (staged)。"
            read -p "确认执行? (y/n): " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                if git reset HEAD~1 --soft; then
                    success_msg "已撤销最近一次 commit，改动已退回暂存区。"
                else
                    error_msg "撤销失败。"
                fi
            fi
            ;;
        2)
            warn_msg "将撤销最近一次 commit，改动退回工作区 (unstaged)。"
            read -p "确认执行? (y/n): " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                if git reset HEAD~1 --mixed; then
                    success_msg "已撤销最近一次 commit，改动已退回工作区。"
                else
                    error_msg "撤销失败。"
                fi
            fi
            ;;
        3)
            warn_msg "⚠ 高危：将丢弃工作区全部未暂存的改动，且不可恢复！"
            read -p "确认丢弃? (y/n): " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                if git restore .; then
                    success_msg "工作区已恢复到最近一次提交的状态。"
                else
                    error_msg "操作失败。"
                fi
            fi
            ;;
        4)
            read -p "请输入要丢弃改动的文件路径: " file_path
            if [ -n "$file_path" ]; then
                warn_msg "⚠ 将丢弃 '$file_path' 的未暂存改动，且不可恢复！"
                read -p "确认? (y/n): " confirm
                if [[ "$confirm" =~ ^[Yy]$ ]]; then
                    if git restore "$file_path"; then
                        success_msg "已丢弃 $file_path 的改动。"
                    else
                        error_msg "操作失败，请检查文件路径是否正确。"
                    fi
                fi
            else
                error_msg "文件路径不能为空。"
                return 1
            fi
            ;;
        5)
            read -p "请输入要取消暂存的文件路径: " file_path
            if [ -n "$file_path" ]; then
                if git restore --staged "$file_path"; then
                    success_msg "已将 $file_path 从暂存区移回工作区。"
                else
                    error_msg "操作失败，请检查文件路径是否正确。"
                fi
            else
                error_msg "文件路径不能为空。"
                return 1
            fi
            ;;
        6)
            return 0
            ;;
        *)
            error_msg "无效选项"
            return 1
            ;;
    esac
}

# 15. NEW: Git 身份配置 (Config)
git_config() {
    title_msg "🔧 Git 身份配置 (Config)"

    local cur_name cur_email
    cur_name=$(git config --global user.name 2>/dev/null)
    cur_email=$(git config --global user.email 2>/dev/null)

    echo -e "当前全局 user.name  : ${CYAN}${cur_name:-未设置}${NC}"
    echo -e "当前全局 user.email : ${CYAN}${cur_email:-未设置}${NC}"
    echo ""
    echo "1) 修改 user.name"
    echo "2) 修改 user.email"
    echo "3) 查看完整的全局 Git 配置"
    echo "4) 返回主菜单"
    read -p "请选择操作: " c_choice

    case $c_choice in
        1)
            read -p "请输入新的 user.name: " new_name
            if [ -n "$new_name" ]; then
                git config --global user.name "$new_name"
                success_msg "user.name 已更新为: $new_name"
            else
                error_msg "名称不能为空"
            fi
            ;;
        2)
            read -p "请输入新的 user.email: " new_email
            if [ -n "$new_email" ]; then
                git config --global user.email "$new_email"
                success_msg "user.email 已更新为: $new_email"
            else
                error_msg "邮箱不能为空"
            fi
            ;;
        3)
            echo ""
            git config --global --list
            ;;
        4)
            return 0
            ;;
        *)
            error_msg "无效选项"
            ;;
    esac
}

# 16. NEW: 克隆仓库 (Clone)
clone_repo() {
    title_msg "📥 克隆仓库 (Clone)"

    echo -e "预设仓库地址: ${CYAN}$MY_REPO_URL${NC}"
    echo ""
    echo "1) 克隆到当前目录下 (自动创建子文件夹)"
    echo "2) 克隆到指定路径"
    echo "3) 返回主菜单"
    read -p "请选择操作: " cl_choice

    case $cl_choice in
        1)
            info_msg "正在克隆 $MY_REPO_URL ..."
            if git clone "$MY_REPO_URL"; then
                success_msg "克隆成功！"
                return 0
            else
                error_msg "克隆失败，请检查网络或仓库地址。"
                return 1
            fi
            ;;
        2)
            read -p "请输入目标路径: " target_path
            if [ -n "$target_path" ]; then
                info_msg "正在克隆到 $target_path ..."
                if git clone "$MY_REPO_URL" "$target_path"; then
                    success_msg "克隆成功！目录: $target_path"
                    return 0
                else
                    error_msg "克隆失败，请检查网络或路径。"
                    return 1
                fi
            else
                error_msg "路径不能为空"
                return 1
            fi
            ;;
        3)
            return 0
            ;;
        *)
            error_msg "无效选项"
            return 1
            ;;
    esac
}

# ================= 终端前端 GUI / 菜单仪表盘 =================
show_dashboard() {
    clear 2>/dev/null || printf '\033[2J\033[H'
    echo -e "${BOLD}══════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${PURPLE}        🛠️  Git Master 控制台  ${NC}"
    echo -e "${BOLD}══════════════════════════════════════════════${NC}"

    echo -e " 📍 物理坐标: ${CYAN}$(pwd)${NC}"

    if check_git_repo; then
        local b_name changes remote
        b_name=$(git branch --show-current 2>/dev/null)
        # local changes
        changes=$(git status --porcelain 2>/dev/null | wc -l)
        # local remote
        remote=$(git remote get-url origin 2>/dev/null || echo "未绑定远程")

        echo -e " 🌿 当前分支: ${GREEN}$b_name${NC}"
        echo -e " 🔗 远程目标: ${CYAN}$remote${NC}"

        if [ "$changes" -gt 0 ]; then
            echo -e " 📝 变动预警: ${YELLOW}工作区有 $changes 个变更未处理${NC}"
        else
            echo -e " 📝 变动预警: ${GREEN}工作区完全纯净${NC}"
        fi
    else
        echo -e " ${YELLOW}⚠️  存储核心: 未检测到 Git 数据库${NC}"
    fi

    echo -e "${BOLD}──────────────────────────────────────────────${NC}"
    echo -e " [1]  📝 暂存变动   (Git Add)"
    echo -e " [2]  📦 创建快照   (Git Commit)"
    echo -e " [3]  🚀 推送云端   (Git Push)"
    echo -e " [4]  📥 拉取更新   (Git Pull)"
    echo -e " [5]  🌿 分支管理   (Branch)"
    echo -e " [6]  📊 状态明细   (Status & Diff)"
    echo -e " [7]  📜 历史查询   (Log Graph)"
    echo -e " [8]  🔗 绑定源址   (Bind Remote)"
    echo -e " [9]  🧙 初始化向导 (Init + Config + Bind)"
    echo -e " [10] 📁 切换目录   (Change Dir)"
    echo -e " [11] 🧹 深度清理   (Git GC)"
    echo -e " [12] 📦 暂存管理   (Stash Save/Pop/Drop)"
    echo -e " [13] ⚡ 一键同步   (Stash→Pull→Pop→Add→Commit→Push)"
    echo -e " [14] ↩️ 撤销操作   (Undo/Reset/Restore)"
    echo -e " [15] 🔧 身份配置   (Git Config)"
    echo -e " [16] 📥 克隆仓库   (Clone)"
    echo -e " [0]  ❌ 退出终端   (Exit)"
    echo -e "${BOLD}══════════════════════════════════════════════${NC}"
}

# ================= 权限前置防线 =================
if [ "$(id -u)" -ne 0 ]; then
    warn_msg "环境提示：未检测到 Root 权限，针对根目录等高权区域可能会读写受阻。"
fi

check_git

# ================= 命令行外置参数解析路由器 =================
if [ $# -gt 0 ]; then
    case "$1" in
        add)    do_add ;;
        commit) do_commit ;;
        push)   do_push ;;
        pull)   do_pull ;;
        branch) manage_branches ;;
        status) view_status ;;
        log)    view_logs ;;
        bind)   bind_remote ;;
        init)   init_wizard ;;
        cd)     change_dir ;;
        clean)  deep_clean ;;
        stash)  manage_stash ;;
        sync)   do_one_click ;;
        undo)   undo_changes ;;
        config) git_config ;;
        clone)  clone_repo ;;
        help|-h|--help)
            echo -e "Git Master CLI 独立模式使用指南:"
            echo -e "  add    : 暂存当前所有改动"
            echo -e "  commit : 为暂存的内容创建快照"
            echo -e "  push   : 将本地提交推送到远程仓库"
            echo -e "  pull   : 拉取远程最新版本"
            echo -e "  branch : 分支管理"
            echo -e "  status : 查看仓库状态"
            echo -e "  log    : 查看提交历史"
            echo -e "  bind   : 绑定远程地址"
            echo -e "  init   : 初始化向导 (Init + Config + Bind)"
            echo -e "  clean  : 深度清理"
            echo -e "  stash  : 暂存管理 (Save/Pop/Drop)"
            echo -e "  sync   : 一键同步"
            echo -e "  undo   : 撤销操作 (Reset/Restore)"
            echo -e "  config : Git 身份配置"
            echo -e "  clone  : 克隆仓库"
            ;;
        *) error_msg "未识别的参数: $1" ;;
    esac
    exit 0
fi

# ================= 交互式生命周期循环 =================
while true; do
    show_dashboard
    read -p "👉 键入数字并回车: " choice

    # FIX: 移除原版 case 里的 [ $? -eq 0 ] 死代码
    # 逻辑：子菜单/查看类操作始终暂停；写操作成功后自动刷新
    require_pause=true
    
    case $choice in
        1)  do_add ;;
        2)  do_commit ;;
        3)  do_push ;;
        4)  do_pull ;;
        5)  manage_branches ;;
        6)  view_status ;;
        7)  view_logs ;;
        8)  bind_remote   && require_pause=false ;;
        9)  init_wizard   && require_pause=false ;;
        10) change_dir    && require_pause=false ;;
        11) deep_clean    && require_pause=false ;;
        12) manage_stash ;;
        13) do_one_click ;;
        14) undo_changes ;;
        15) git_config ;;
        16) clone_repo ;;
        0)  echo "控制台已下线。"; exit 0 ;;
        *)  error_msg "非法的选项指令，请确认您输入的数字有效" ;;
    esac
    
    echo ""
    if [ "$require_pause" = true ]; then
        # 失败、或者执行查看类操作时，要求按回车以便查阅终端内容
        read -p "按 [Enter] 键继续..."
    else
        # 成功完成操作时，停留一小会儿让用户看清成功提示，然后自动刷新面板
        # FIX: sleep 1.5 不符合 POSIX，部分系统不支持小数，改为 sleep 2
        info_msg "操作成功完成，即将自动返回主菜单..."
        sleep 2
    fi
done
