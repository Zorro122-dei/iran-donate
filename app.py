    <script>
        // --- Матричный фон ---
        const c=document.getElementById('m'), x=c.getContext('2d');
        c.width=window.innerWidth; c.height=window.innerHeight;
        const d=Array(Math.floor(c.width/20)).fill(1);
        function draw(){
            x.fillStyle='rgba(26,26,26,0.1)'; x.fillRect(0,0,c.width,c.height);
            x.fillStyle='#f00'; x.font='15px monospace';
            d.forEach((y,i)=>{
                x.fillText(Math.floor(Math.random()*2),i*20,y*20);
                if(y*20>c.height&&Math.random()>0.975)d[i]=0;
                d[i]++;
            });
        }
        setInterval(draw, 50);

        // --- Логика шкалы (Progress Bar) с сохранением ---
        function updateProgress() {
            const storageKey = 'fund_progress_value';
            const startInitial = 18.4100;
            
            // Загружаем сохраненное значение или ставим стартовое
            let currentVal = parseFloat(localStorage.getItem(storageKey)) || startInitial;

            const display = document.getElementById('p');
            const bar = document.getElementById('f');

            // Функция обновления визуальной части
            const refreshUI = (val) => {
                display.innerText = val.toFixed(4);
                bar.style.width = (val > 100 ? 100 : val) + '%';
            };

            refreshUI(currentVal);

            // Медленный рост каждые 2 секунды
            setInterval(() => {
                currentVal += Math.random() * 0.0002; // Скорость роста
                localStorage.setItem(storageKey, currentVal); // Сохраняем в браузер
                refreshUI(currentVal);
            }, 2000);
        }
        updateProgress();

        // --- Копирование адреса ---
        function copyIt(id) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText);
            el.classList.add('highlight');
            setTimeout(() => { el.classList.remove('highlight'); }, 200);
        }

        // --- Лента транзакций (каждые 25-40 секунд) ---
        function add(){
            const l=document.getElementById('l'), e=document.createElement('div');
            e.innerHTML=`[${new Date().toLocaleTimeString()}] Incoming confirmed: +${(Math.random()*0.01).toFixed(3)} BTC...`;
            l.prepend(e); 
            if(l.childNodes.length > 5) l.removeChild(l.lastChild);

            // Планируем следующее появление через случайное время (25-40 сек)
            const nextTime = Math.floor(Math.random() * (40000 - 25000 + 1) + 25000);
            setTimeout(add, nextTime);
        }
        
        // Первый запуск ленты
        setTimeout(add, 2000); 
    </script>
