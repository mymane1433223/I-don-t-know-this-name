// 更新显示的函数
function updateDisplay(data) {
    // 更新时间戳
    document.getElementById('last-update').textContent = new Date().toLocaleString();
    
    // 更新服务器变量显示
    document.getElementById('server-vars').textContent = 
        JSON.stringify(data.server_vars, null, 2);
    
    // 更新局部变量显示
    document.getElementById('local-vars').textContent = 
        JSON.stringify(data.local_vars, null, 2);
    
    // 更新全局变量显示
    document.getElementById('global-vars').textContent = 
        JSON.stringify(data.global_vars, null, 2);
}

// 从服务器获取数据的函数
function fetchData() {
    fetch('/get_vars')
        .then(response => response.json())
        .then(data => {
            updateDisplay(data);
        })
        .catch(error => {
            console.error('获取数据失败:', error);
        });
}

// 每0.5秒获取一次数据
setInterval(fetchData, 500);

// 初始加载时立即获取一次数据
fetchData();