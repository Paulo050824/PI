PRAGMA foreign_keys = ON;

--
-- Estrutura da tabela `tatuagem`
--
DROP TABLE IF EXISTS `tatuagem`;
CREATE TABLE `tatuagem` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nome` TEXT NOT NULL,
  `preco` NUMERIC NOT NULL,
  `tamanho` NUMERIC NOT NULL,
  `imagem` TEXT DEFAULT NULL,
  `descricao` TEXT
);

--
-- Inserção de dados na tabela `tatuagem`
--
INSERT INTO `tatuagem` (`id`, `nome`, `preco`, `tamanho`, `imagem`, `descricao`) VALUES 
(3, 'Rosa com Borboletas e Frase', 0.00, 25.00, 'tattoo_flores_e_borboletas.png', 'Rosa central acompanhada de pequenas borboletas, folhas e uma frase escrita verticalmente nas costas.'),
(4, 'Jardim de Flores e Borboletas', 0.00, 25.00, 'tattoo_flores.png', 'Composição vertical de flores, folhas e borboletas em traço fino, delicada e detalhada.'),
(5, 'Coroa e Homenagem Real', 0.00, 25.00, 'tattoo_coroa.png', 'Tatuagem masculina personalizada com coroa, mãos, nome, data e elementos simbólicos de nascimento/homenagem.'),
(6, 'Jardim de Borboletas', 0.00, 30.00, 'tattoo_flores_e_borboletas_2.png', 'Composição delicada de flores, folhas e borboletas em estilo fine line, distribuída verticalmente pelo braço, com detalhes em sombreamento.'),
(7, 'Samurai da Morte', 0.00, 30.00, 'tattoo_paulo.png', '- Tatuagem realista de uma caveira com armadura e capacete de samurai, acompanhada de outras caveiras menores e detalhes em preto, cinza e pequenos toques de vermelho.');

--
-- Estrutura da tabela `avaliacoes`
--
DROP TABLE IF EXISTS `avaliacoes`;
CREATE TABLE `avaliacoes` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `id_tatuagem` INTEGER NOT NULL,
  `cliente` TEXT NOT NULL,
  `nota` NUMERIC NOT NULL,
  FOREIGN KEY (`id_tatuagem`) REFERENCES `tatuagem` (`id`) ON DELETE CASCADE
);

CREATE INDEX `idx_avaliacoes_id_tatuagem` ON `avaliacoes` (`id_tatuagem`);

--
-- Estrutura da tabela `catalogos`
--
DROP TABLE IF EXISTS `catalogos`;
CREATE TABLE `catalogos` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nome` TEXT NOT NULL,
  `id_tatuagem` INTEGER NOT NULL
);

--
-- Estrutura da tabela `usuario`
--
DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nome` TEXT NOT NULL,
  `email` TEXT NOT NULL UNIQUE,
  `senha_hash` TEXT NOT NULL,
  `is_admin` INTEGER NOT NULL DEFAULT 0
);

--
-- Inserção de dados na tabela `usuario`
--
INSERT INTO `usuario` (`id`, `nome`, `email`, `senha_hash`, `is_admin`) VALUES 
(1, 'Paulo Roberto', 'santosnetopaulo90@gmail.com', 'scrypt:32768:8:1$7FF3qoX0OC2iHRrZ$e634a1e99e2eefbb08581e488362cb70fba9010a00c615bcba9f33acebb310ace98bb36e9ccd089ce9d17668dcad8ead620269331a508e30d097cf758c175289', 1);