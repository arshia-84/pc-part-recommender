import re 
import requests
import csv 
import io 

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def cpu(cpu_budget):

    ram_url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/cpu.csv'
    ram_response = requests.get(ram_url, headers=HEADER)
    ram_reader = csv.DictReader(io.StringIO(ram_response.text)) 
    ram_rows = list(ram_reader)

    MA = {}

    for row in ram_rows : 
        MA[row['name']] = row['microarchitecture']


    value_url = 'https://www.cpubenchmark.net/cpu_value_available.html'

    value_response = requests.get(value_url, headers=HEADER)
    model_pattern = re.compile(r'<span class="prdname">(.*?)</span>')
    price_pattern = re.compile(r'<span class="price-neww">(.*?)</span>')

    models = model_pattern.findall(value_response.text) 
    prices = price_pattern.findall(value_response.text)

    cpus = {}

    for model , price in zip(models, prices):
        cpus[model] = float(price.replace('$','').replace(',','').strip())

    gaming_url = 'https://www.cpubenchmark.net/top-gaming-cpus.html'

    gaming_response = requests.get(gaming_url, headers=HEADER)

    gaming_models = model_pattern.findall(gaming_response.text)

    found = False 

    for model in gaming_models : 
        try : 
            if cpus[model] <= cpu_budget and MA[model]: 
                print(f'[CPU] {model} — ${cpus[model]:.2f} within budget') 
                
                return MA[model] , model, cpus[model] 
        except (ValueError, KeyError):
            continue 

    print("No CPU found within budget.\nIncrease your budget.")
    exit()


def gpu(gpu_budget):
    gpu_url = 'https://www.videocardbenchmark.net/high_end_gpus.html'
    gpu_name_response = requests.get(gpu_url, headers=HEADER)

    gpu_name_pattern = re.compile(r'<span class="prdname" >(.*?)</span>')
    gpu_price_pattern = re.compile(r'<span class="price-neww" >(.*?)</span>')  # underscore

    gpu_names = gpu_name_pattern.findall(gpu_name_response.text)
    gpu_prices = gpu_price_pattern.findall(gpu_name_response.text)

    for gpu_name, raw_price in zip(gpu_names, gpu_prices):
        try:
            price = float(raw_price.replace('$', '').replace(',', '').replace('*', '').strip())
        except ValueError:
            continue

        if price <= gpu_budget:
            print(f'[GPU] {gpu_name} — ${price:.2f} within budget')
            return gpu_name, price 

    print("No GPU found within budget.\nIncrease your budget.")

    exit()

def ram(ram_budget, microarchitecture):
    MEMORY_TYPE = {
        # Intel
        'Raptor Lake Refresh': 'DDR4/DDR5',
        'Raptor Lake': 'DDR4/DDR5',
        'Alder Lake': 'DDR4/DDR5',
        'Arrow Lake': 'DDR5',
        'Rocket Lake': 'DDR4',
        'Comet Lake': 'DDR4',
        'Coffee Lake Refresh': 'DDR4',
        'Coffee Lake': 'DDR4',
        'Kaby Lake': 'DDR4',
        'Skylake': 'DDR4',
        'Haswell Refresh': 'DDR3',
        'Haswell': 'DDR3',
        'Ivy Bridge': 'DDR3',
        'Sandy Bridge': 'DDR3',
        'Broadwell': 'DDR3',
        'Cascade Lake': 'DDR4',
        'Westmere': 'DDR3',
        'Nehalem': 'DDR3',
        'Wolfdale': 'DDR2/DDR3',
        'Yorkfield': 'DDR2/DDR3',
        'Core': 'DDR2',
        'Lynx': 'DDR3',

        # AMD
        'Zen 5': 'DDR5',
        'Zen 4': 'DDR5',
        'Zen 3': 'DDR4',
        'Zen 2': 'DDR4',
        'Zen+': 'DDR4',
        'Zen': 'DDR4',
        'Piledriver': 'DDR3',
        'Bulldozer': 'DDR3',
        'Steamroller': 'DDR3',
        'Excavator': 'DDR3',
        'Puma+': 'DDR3',
        'Jaguar': 'DDR3',
        'K10': 'DDR2/DDR3',
    }

    url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/memory.csv'

    response = requests.get(url, headers=HEADER)
    reader = csv.DictReader(io.StringIO(response.text)) 
    rows = list(reader)

    rows = [x for x in rows if x['price'].strip()]

    rows.sort(key=lambda x : (
        -int(x['speed'][2:] or 0),
        float(x['cas_latency'] or 0),
        float(x['price'] or 0) 
    ))

    for row in rows : 
        try : 
            price = float(row['price'])
            name = row['name']
            mem_type = MEMORY_TYPE.get(microarchitecture, 'DDR4')
        except (ValueError, KeyError) : 
            continue 

        if price <= ram_budget and (row['speed'][0] in mem_type) : 
            print(f'[RAM] {name} DDR{row['speed'][0]} — ${price:.2f} within budget')
            return name , price
    print("No RAM found within budget.\nIncrease your budget.")
    exit() 

def Disk(disk_budget):
    for page in range(1, 21):
        disk_url = f'https://www.harddrivebenchmark.net/drives/page{page}'
        disk_name_response = requests.get(disk_url, headers=HEADER)

        disk_name_pattern = re.compile(r'<span class="prdname" >(.*?)</span>')
        disk_price_pattern = re.compile(r'<span class="price-neww" >(.*?)</span>')

        disk_names = disk_name_pattern.findall(disk_name_response.text)
        disk_prices = disk_price_pattern.findall(disk_name_response.text)

        for disk_name, raw_price in zip(disk_names, disk_prices):
            try:
                price = float(raw_price.replace('$', '').replace(',', '').replace('*', '').strip())
            except ValueError:
                continue

            if price <= disk_budget:
                print(f'[DISK] {disk_name} — ${price:.2f} within budget')
                return disk_name, price

    print("No DISK found within budget.\nIncrease your budget.")
    exit()

def main():
    total_spent = 0 
    budget = float(input('Enter Budget(USD): '))
    
    disk_name, disk_price = Disk((budget*10)/100)
    total_spent += disk_price
    cpu_microarcitecture , cpu_name, cpu_price = cpu(((budget - total_spent) * 25)/100)
    total_spent += cpu_price
    ram_name, ram_price = ram(((budget - total_spent)* 15) / 100, cpu_microarcitecture)
    total_spent += ram_price
    gpu_name, gpu_price = gpu(budget - total_spent)
    total_spent += gpu_price
    remain = budget - total_spent
    print(f'[SPENT] ${total_spent:.2f}\n[REMAIN] ${remain:.2f}')

    fields = ['cpu_name','cpu_price','gpu_name', 'gpu_price', 'ram_name', 'ram_price', 'disk_name', 'disk_price', 'remain']

    rows = [cpu_name,round(cpu_price, 2), gpu_name, round(gpu_price, 2), ram_name, round(ram_price, 2), disk_name, round(disk_price, 2), round(remain, 2)]

    with open('pc-part-recommender.csv', 'w', newline='') as f : 
        writer = csv.writer(f)
        writer.writerow(fields) 
        writer.writerow(rows)


if __name__ == '__main__':
    main()