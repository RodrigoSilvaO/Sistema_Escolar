-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 20/08/2026 às 02:18
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `sistema_escolar`
--
CREATE DATABASE IF NOT EXISTS `sistema_escolar` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `sistema_escolar`;

-- --------------------------------------------------------

--
-- Estrutura para tabela `aluno`
--

DROP TABLE IF EXISTS `aluno`;
CREATE TABLE IF NOT EXISTS `aluno` (
  `id_aluno` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `data_nascimento` date NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `data_matricula` date NOT NULL,
  PRIMARY KEY (`id_aluno`),
  KEY `idx_aluno_nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `avaliacao`
--

DROP TABLE IF EXISTS `avaliacao`;
CREATE TABLE IF NOT EXISTS `avaliacao` (
  `id_boletim` int(11) NOT NULL AUTO_INCREMENT,
  `observacao` varchar(255) DEFAULT NULL,
  `numero_avaliacao` tinyint(3) UNSIGNED NOT NULL,
  `nota` decimal(5,2) DEFAULT NULL,
  `data_avaliacao` date NOT NULL,
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  PRIMARY KEY (`id_boletim`),
  KEY `fk_avaliacao_aluno` (`id_aluno`),
  KEY `fk_avaliacao_disciplina` (`id_disciplina`),
  KEY `idx_avaliacao_data` (`id_disciplina`,`data_avaliacao`)
) ;

--
-- Acionadores `avaliacao`
--
DROP TRIGGER IF EXISTS `trg_atualiza_resultado_final`;
DELIMITER $$
CREATE TRIGGER `trg_atualiza_resultado_final` AFTER INSERT ON `avaliacao` FOR EACH ROW BEGIN
    DECLARE v_media DECIMAL(5,2);
    DECLARE v_situacao ENUM('Aprovado','Reprovado','Recuperacao');

    SELECT AVG(nota) INTO v_media
    FROM avaliacao
    WHERE id_aluno = NEW.id_aluno AND id_disciplina = NEW.id_disciplina;

    IF v_media >= 7.0 THEN
        SET v_situacao = 'Aprovado';
    ELSEIF v_media >= 5.0 THEN
        SET v_situacao = 'Recuperacao';
    ELSE
        SET v_situacao = 'Reprovado';
    END IF;

    INSERT INTO resultado_final (id_aluno, id_disciplina, situacao, frequencia)
    VALUES (NEW.id_aluno, NEW.id_disciplina, v_situacao, 'Presente')
    ON DUPLICATE KEY UPDATE situacao = v_situacao;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `disciplina`
--

DROP TABLE IF EXISTS `disciplina`;
CREATE TABLE IF NOT EXISTS `disciplina` (
  `id_disciplina` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `carga_horaria` smallint(5) UNSIGNED NOT NULL,
  `tipo` varchar(50) NOT NULL,
  PRIMARY KEY (`id_disciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `disciplina_professor`
--

DROP TABLE IF EXISTS `disciplina_professor`;
CREATE TABLE IF NOT EXISTS `disciplina_professor` (
  `id_professor` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  PRIMARY KEY (`id_professor`,`id_disciplina`),
  KEY `fk_dp_disciplina` (`id_disciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `especialidade_professor`
--

DROP TABLE IF EXISTS `especialidade_professor`;
CREATE TABLE IF NOT EXISTS `especialidade_professor` (
  `id_especialidade` int(11) NOT NULL AUTO_INCREMENT,
  `especialidade` varchar(100) NOT NULL,
  PRIMARY KEY (`id_especialidade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `matricula_disciplina`
--

DROP TABLE IF EXISTS `matricula_disciplina`;
CREATE TABLE IF NOT EXISTS `matricula_disciplina` (
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `id_turma` int(11) NOT NULL,
  PRIMARY KEY (`id_aluno`,`id_disciplina`,`id_turma`),
  KEY `fk_md_disciplina` (`id_disciplina`),
  KEY `fk_md_turma` (`id_turma`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `periodo_ferias`
--

DROP TABLE IF EXISTS `periodo_ferias`;
CREATE TABLE IF NOT EXISTS `periodo_ferias` (
  `id_ferias` int(11) NOT NULL AUTO_INCREMENT,
  `id_periodo` int(11) NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date NOT NULL,
  PRIMARY KEY (`id_ferias`),
  KEY `fk_ferias_periodo` (`id_periodo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `periodo_letivo`
--

DROP TABLE IF EXISTS `periodo_letivo`;
CREATE TABLE IF NOT EXISTS `periodo_letivo` (
  `id_periodo` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date NOT NULL,
  PRIMARY KEY (`id_periodo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `professor`
--

DROP TABLE IF EXISTS `professor`;
CREATE TABLE IF NOT EXISTS `professor` (
  `id_professor` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `id_especialidade` int(11) NOT NULL,
  PRIMARY KEY (`id_professor`),
  KEY `fk_professor_especialidade` (`id_especialidade`),
  KEY `idx_professor_nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `registro_frequencia`
--

DROP TABLE IF EXISTS `registro_frequencia`;
CREATE TABLE IF NOT EXISTS `registro_frequencia` (
  `id_frequencia` int(11) NOT NULL AUTO_INCREMENT,
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `data_aula` date NOT NULL,
  `status_presenca` enum('Presente','Ausente','Justificada') NOT NULL,
  PRIMARY KEY (`id_frequencia`),
  KEY `fk_frequencia_aluno` (`id_aluno`),
  KEY `fk_frequencia_disciplina` (`id_disciplina`),
  KEY `idx_frequencia_busca` (`id_disciplina`,`data_aula`,`status_presenca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `resultado_final`
--

DROP TABLE IF EXISTS `resultado_final`;
CREATE TABLE IF NOT EXISTS `resultado_final` (
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `situacao` enum('Aprovado','Reprovado','Recuperacao') NOT NULL,
  `frequencia` enum('Presente','Ausente','Justificado') NOT NULL,
  PRIMARY KEY (`id_aluno`,`id_disciplina`),
  KEY `fk_resultado_disciplina` (`id_disciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `turma`
--

DROP TABLE IF EXISTS `turma`;
CREATE TABLE IF NOT EXISTS `turma` (
  `id_turma` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `id_periodo` int(11) NOT NULL,
  PRIMARY KEY (`id_turma`),
  KEY `fk_turma_periodo` (`id_periodo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `turma_disciplina`
--

DROP TABLE IF EXISTS `turma_disciplina`;
CREATE TABLE IF NOT EXISTS `turma_disciplina` (
  `id_turma` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `id_professor` int(11) NOT NULL,
  PRIMARY KEY (`id_turma`,`id_disciplina`,`id_professor`),
  KEY `fk_td_disciplina` (`id_disciplina`),
  KEY `fk_td_professor` (`id_professor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `vw_lista_presenca`
-- (Veja abaixo para a visão atual)
--
DROP VIEW IF EXISTS `vw_lista_presenca`;
CREATE TABLE IF NOT EXISTS `vw_lista_presenca` (
`id_aluno` int(11)
,`nome` varchar(50)
,`disciplina` varchar(100)
);

-- --------------------------------------------------------

--
-- Estrutura para view `vw_lista_presenca`
--
DROP TABLE IF EXISTS `vw_lista_presenca`;

DROP VIEW IF EXISTS `vw_lista_presenca`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_lista_presenca`  AS SELECT `a`.`id_aluno` AS `id_aluno`, `a`.`nome` AS `nome`, `d`.`nome` AS `disciplina` FROM ((`aluno` `a` join `registro_frequencia` `f` on(`a`.`id_aluno` = `f`.`id_aluno`)) join `disciplina` `d` on(`f`.`id_disciplina` = `d`.`id_disciplina`)) ;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `avaliacao`
--
ALTER TABLE `avaliacao`
  ADD CONSTRAINT `fk_avaliacao_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`),
  ADD CONSTRAINT `fk_avaliacao_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`);

--
-- Restrições para tabelas `disciplina_professor`
--
ALTER TABLE `disciplina_professor`
  ADD CONSTRAINT `fk_dp_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`),
  ADD CONSTRAINT `fk_dp_professor` FOREIGN KEY (`id_professor`) REFERENCES `professor` (`id_professor`);

--
-- Restrições para tabelas `matricula_disciplina`
--
ALTER TABLE `matricula_disciplina`
  ADD CONSTRAINT `fk_md_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`),
  ADD CONSTRAINT `fk_md_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`),
  ADD CONSTRAINT `fk_md_turma` FOREIGN KEY (`id_turma`) REFERENCES `turma` (`id_turma`);

--
-- Restrições para tabelas `periodo_ferias`
--
ALTER TABLE `periodo_ferias`
  ADD CONSTRAINT `fk_ferias_periodo` FOREIGN KEY (`id_periodo`) REFERENCES `periodo_letivo` (`id_periodo`);

--
-- Restrições para tabelas `professor`
--
ALTER TABLE `professor`
  ADD CONSTRAINT `fk_professor_especialidade` FOREIGN KEY (`id_especialidade`) REFERENCES `especialidade_professor` (`id_especialidade`);

--
-- Restrições para tabelas `registro_frequencia`
--
ALTER TABLE `registro_frequencia`
  ADD CONSTRAINT `fk_frequencia_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`),
  ADD CONSTRAINT `fk_frequencia_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`);

--
-- Restrições para tabelas `resultado_final`
--
ALTER TABLE `resultado_final`
  ADD CONSTRAINT `fk_resultado_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`),
  ADD CONSTRAINT `fk_resultado_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`);

--
-- Restrições para tabelas `turma`
--
ALTER TABLE `turma`
  ADD CONSTRAINT `fk_turma_periodo` FOREIGN KEY (`id_periodo`) REFERENCES `periodo_letivo` (`id_periodo`);

--
-- Restrições para tabelas `turma_disciplina`
--
ALTER TABLE `turma_disciplina`
  ADD CONSTRAINT `fk_td_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`),
  ADD CONSTRAINT `fk_td_professor` FOREIGN KEY (`id_professor`) REFERENCES `professor` (`id_professor`),
  ADD CONSTRAINT `fk_td_turma` FOREIGN KEY (`id_turma`) REFERENCES `turma` (`id_turma`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
