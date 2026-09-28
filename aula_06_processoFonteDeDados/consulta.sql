-- SQLite
SELECT  municipio,
        descricao_tipo_unidade,
        COUNT(*) as n
FROM estabelecimentos
WHERE 
    descricao_tipo_unidade IN ('HOSPITAL GERAL', 'CENTRO DE SAUDE/UNIDADE BASICA')
GROUP BY municipio,descricao_tipo_unidade
ORDER BY n DESC;

    
