#!/usr/bin/env julia

# TODO: use ARGV to pass name or at least number of Leja points.
N = 500
ps = Array{Float64}(undef, N)
fname = "divd-diff-exp_N" * string(N) * ".dat"
open(fname, "r") do f
  read!(f, ps)
end

println("ps length: ", length(ps))
println(ps)
