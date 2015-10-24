library(RcppCNPy)

edge_names= c(
    "white-white",
    "black-white",
    "hispanic-white",
    "black-black",
    "hispanic-black",
    "hispanic-hispanic")

for (edge in edge_names) {
    filename = paste(edge, '.npy', sep = '')
    print(npyLoad(filename))
}
