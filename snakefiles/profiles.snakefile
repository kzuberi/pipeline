

FNS = glob_wildcards("data/networks/profile/{collection}/{fn}.txt")


rule PROFILES:
    message: "target rule for interaction networks created from profile data"
    input: expand("work/networks/profile/{collection}/{fn}.txt.nn", zip, collection=FNS.collection, fn=FNS.fn)

rule PROCESS_PROFILES_P2N:
    message: "convert profiles to networks"
    input: data="data/networks/profile/{collection}/{fn}.txt", mapping="work/identifiers/symbols.txt"
    output: "work/networks/profile/{collection}/{fn}.txt.p2n"
    log: "work/networks/profile/{collection}/{fn}.txt.p2n.log"
    params: proftype='continuous', cor="pearson", threshold="auto"
    shell: 'java -Xmx1G -cp {JAR_FILE} org.genemania.engine.core.evaluation.ProfileToNetworkDriver \
        -in "{input.data}" -out "{output}" -log "{log}" -syn "{input.mapping}" \
        -proftype {params.proftype} -cor {params.cor} -threshold {params.threshold} \
        -keepAllTies -limitTies'

rule PROCESS_PROFILES_NN:
    message: "network normalization"
    input: data="work/networks/profile/{collection}/{fn}.txt.p2n", mapping="work/identifiers/symbols.txt"
    output: "work/networks/profile/{collection}/{fn}.txt.nn"
    log: "work/networks/profile/{collection}/{fn}.txt.nn.log"
    shell: 'java -Xmx512m -cp {JAR_FILE}  org.genemania.engine.apps.NetworkNormalizer -outtype uid -norm true  -in "{input.data}" -out "{output}" -log "{log}" -syn "{input.mapping}"'

rule CLEAN_PROFILES:
    shell: """
    rm -rf work/networks/profile/*
    """
