import subprocess

base_dir = 'julia-fn/'

subprocess.run(['julia', base_dir+'gen-lp.jl'])
result = subprocess.run(['julia', base_dir+'read-lp.jl'], stdout=subprocess.PIPE)
result = result.stdout.decode('utf-8')
print(result)


# divd-diff-calc.jl
# read-dde.jl
subprocess.run(['julia', base_dir+'divd-diff-calc.jl'])
result = subprocess.run(['julia', base_dir+'read-dde.jl'], stdout=subprocess.PIPE)
result = result.stdout.decode('utf-8')
print(result)