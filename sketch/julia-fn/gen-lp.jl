#!/usr/bin/julia

a = 0.0
b = 1.0

function fLP(x, ps)
  p = 1
  for k in ps
    p = p*(x-k)
  end
  return abs(p)
end

function diff(x, d, ps)
  return (fLP(x+d,ps) - fLP(x-d,ps))/(2*d)
end

function find_max(a, b, ps, d, e)
  c = 0.5*(a+b)
  if abs(b-a) < 2*e
    return -1., -1.
  end
  if d > 0.5*(b-a)
    @assert d > 0.5(b-a) "WARNING: we have to decrease delta from " * string(d) * " to value " * string(0.25*()) * " but this is suboptimal and would increase errors."
    d = 0.25*(b-a)
  end
  fd = diff(c, d, ps)
  if abs(fd) < e
    return c, fLP(c, ps)
  end
  if fd > 0
    return find_max(c, b, ps, d, e)
  elseif fd < 0
    return find_max(a, c, ps, d, e)
  end
end

function calc_LP(e, d, n, ser)
  ps = [1., 0., 0.5]
  sps = sort(ps)
  if ser == 1
    x, v = find_max(sps[1], sps[2], ps, d, e)
  else
    x, v = find_max(sps[2], sps[3], ps, d, e)
  end
  push!(ps, x)

  for i = 5:n
    mx = []
    mv = []
    sps = sort(ps)
    for k=1:i-2
      x,v = find_max(sps[k], sps[k+1], ps, d, e)
      if x > 0
        push!(mx, x)
        push!(mv, v)
      end
    end
    point = mx[argmax(mv)]
    val = mv[argmax(mv)]
    push!(ps, point)
  end
  return ps
end

# relation between delta and epsilon: delta \approx epsilon^{1/3}
epsilon = 1e-15
delta   = 1e-5
N       = 127
N       = 500

points = calc_LP(epsilon, delta, N, 1)
#  println(points)
fname = "lp-lb_N" * string(N) * ".dat"
open(fname, "w") do f
  write(f, points)
end

points = calc_LP(epsilon, delta, N, 2)
#  println(points)
fname = "lp-rb_N" * string(N) * ".dat"
open(fname, "w") do f
  write(f, points)
end
