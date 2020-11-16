#!/usr/bin/env julia

# This script precalculates divided differences on Leja points of exp.
# The recursive algorithm would too cost (exponential increase of numbef of functions),
# while linear (ordinary sum) formula is a bit cumbersome while still simple.
# We precompute the denominators storing them in array, as well as the numerator.
#
# read Leja points generated by a 'gen-lp' program.
# file: 'lp-[lr]b_N#.dat' where '#' is number of generated points (julia script quickly generates 500 points).

function denoms(n,ps)
    dns = Array{Float64}(undef, n)
    for i=1:n
        p = 1
        for j=1:n
        if j != i
            p = p*(ps[i] - ps[j])
        end
        end
        dns[i] = p
    end
    return dns
end

function divd_diff(ps)
    dd = Array{Float64}(undef, length(ps))
    dd[1] = exp(ps[1])
    for i=2:length(ps)
        dns = denoms(i,ps)
        nms = exp.(ps)
        dd[i] = sum([nms[k]/dns[k] for k=1:i])
    end
    return dd
end

N = 500
branch = "l"
fname = "lp-" * branch * "b_N" * string(N) * ".dat"

ps = Array{Float64}(undef, N)
open(fname, "r") do f
    read!(f, ps)
end

@assert ps[1] == 1.0 "ERROR: we couldn't successfully read data from file '" * fname * "'"

ds = divd_diff(ps)

ofile = "divd-diff-exp_N" * string(N) * ".dat"
open(ofile, "w") do f
    write(f, ds)
end
