-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 20/08/2026 às 04:11
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

-- --------------------------------------------------------

--
-- Estrutura para tabela `aluno`
--

CREATE TABLE `aluno` (
  `id_aluno` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `data_nascimento` date NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `data_matricula` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `aluno`
--

INSERT INTO `aluno` (`id_aluno`, `nome`, `data_nascimento`, `endereco`, `data_matricula`) VALUES
(2, 'matue', '2026-08-07', 'maconha 1', '2026-08-18');

-- --------------------------------------------------------

--
-- Estrutura para tabela `avaliacao`
--

CREATE TABLE `avaliacao` (
  `id_boletim` int(11) NOT NULL,
  `observacao` varchar(255) DEFAULT NULL,
  `numero_avaliacao` tinyint(3) UNSIGNED NOT NULL,
  `nota` decimal(5,2) DEFAULT NULL,
  `data_avaliacao` date NOT NULL,
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `avaliacao`
--

INSERT INTO `avaliacao` (`id_boletim`, `observacao`, `numero_avaliacao`, `nota`, `data_avaliacao`, `id_aluno`, `id_disciplina`) VALUES
(1, '111', 1, 10.00, '2026-08-07', 2, 1);

--
-- Acionadores `avaliacao`
--
DELIMITER $$
CREATE TRIGGER `trg_atualiza_resultado_after_delete` AFTER DELETE ON `avaliacao` FOR EACH ROW BEGIN
    DECLARE v_media DECIMAL(5,2);
    DECLARE v_situacao ENUM('Aprovado','Reprovado','Recuperacao');
    SELECT AVG(nota) INTO v_media
    FROM avaliacao
    WHERE id_aluno = OLD.id_aluno AND id_disciplina = OLD.id_disciplina;
    IF v_media IS NOT NULL THEN
        IF v_media >= 7.0 THEN
            SET v_situacao = 'Aprovado';
        ELSEIF v_media >= 5.0 THEN
            SET v_situacao = 'Recuperacao';
        ELSE
            SET v_situacao = 'Reprovado';
        END IF;
        UPDATE resultado_final 
        SET situacao = v_situacao
        WHERE id_aluno = OLD.id_aluno AND id_disciplina = OLD.id_disciplina;
    ELSE
        DELETE FROM resultado_final 
        WHERE id_aluno = OLD.id_aluno AND id_disciplina = OLD.id_disciplina;
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_atualiza_resultado_after_update` AFTER UPDATE ON `avaliacao` FOR EACH ROW BEGIN
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
    UPDATE resultado_final 
    SET situacao = v_situacao
    WHERE id_aluno = NEW.id_aluno AND id_disciplina = NEW.id_disciplina;
END
$$
DELIMITER ;
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
DELIMITER $$
CREATE TRIGGER `trg_valida_nota_before_insert` BEFORE INSERT ON `avaliacao` FOR EACH ROW BEGIN
    IF NEW.nota < 0.00 OR NEW.nota > 10.00 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Erro: A nota deve ser um valor entre 0.00 e 10.00.';
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_valida_nota_before_update` BEFORE UPDATE ON `avaliacao` FOR EACH ROW BEGIN
    IF NEW.nota < 0.00 OR NEW.nota > 10.00 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Erro: A nota deve ser um valor entre 0.00 e 10.00.';
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `disciplina`
--

CREATE TABLE `disciplina` (
  `id_disciplina` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `carga_horaria` smallint(5) UNSIGNED NOT NULL,
  `tipo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `disciplina`
--

INSERT INTO `disciplina` (`id_disciplina`, `nome`, `carga_horaria`, `tipo`) VALUES
(1, 'matue ', 1, 'maconha'),
(2, '', 0, '');

-- --------------------------------------------------------

--
-- Estrutura para tabela `disciplina_professor`
--

CREATE TABLE `disciplina_professor` (
  `id_professor` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `especialidade_professor`
--

CREATE TABLE `especialidade_professor` (
  `id_especialidade` int(11) NOT NULL,
  `especialidade` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `especialidade_professor`
--

INSERT INTO `especialidade_professor` (`id_especialidade`, `especialidade`) VALUES
(1, 'apertar o beck'),
(2, 'apertar o beck'),
(3, 'apertar o beck');

-- --------------------------------------------------------

--
-- Estrutura para tabela `matricula_disciplina`
--

CREATE TABLE `matricula_disciplina` (
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `id_turma` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `periodo_ferias`
--

CREATE TABLE `periodo_ferias` (
  `id_ferias` int(11) NOT NULL,
  `id_periodo` int(11) NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `periodo_letivo`
--

CREATE TABLE `periodo_letivo` (
  `id_periodo` int(11) NOT NULL,
  `descricao` varchar(255) NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `professor`
--

CREATE TABLE `professor` (
  `id_professor` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `id_especialidade` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `professor`
--

INSERT INTO `professor` (`id_professor`, `nome`, `id_especialidade`) VALUES
(1, 'maconha ', 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `registro_frequencia`
--

CREATE TABLE `registro_frequencia` (
  `id_frequencia` int(11) NOT NULL,
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `data_aula` date NOT NULL,
  `status_presenca` enum('Presente','Ausente','Justificada') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `registro_frequencia`
--

INSERT INTO `registro_frequencia` (`id_frequencia`, `id_aluno`, `id_disciplina`, `data_aula`, `status_presenca`) VALUES
(1, 2, 1, '0000-00-00', 'Presente'),
(2, 2, 1, '0000-00-00', 'Presente');

--
-- Acionadores `registro_frequencia`
--
DELIMITER $$
CREATE TRIGGER `trg_valida_frequencia_ferias` BEFORE INSERT ON `registro_frequencia` FOR EACH ROW BEGIN
    IF EXISTS (
        SELECT 1 FROM periodo_ferias 
        WHERE NEW.data_aula BETWEEN data_inicio AND data_fim
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Não é permitido registrar frequência em período de férias.';
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `resultado_final`
--

CREATE TABLE `resultado_final` (
  `id_aluno` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `situacao` enum('Aprovado','Reprovado','Recuperacao') NOT NULL,
  `frequencia` enum('Presente','Ausente','Justificado') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `turma`
--

CREATE TABLE `turma` (
  `id_turma` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `id_periodo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `turma_disciplina`
--

CREATE TABLE `turma_disciplina` (
  `id_turma` int(11) NOT NULL,
  `id_disciplina` int(11) NOT NULL,
  `id_professor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `vw_lista_presenca`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `vw_lista_presenca` (
`id_aluno` int(11)
,`nome` varchar(50)
,`disciplina` varchar(100)
);

-- --------------------------------------------------------

--
-- Estrutura para view `vw_lista_presenca`
--
DROP TABLE IF EXISTS `vw_lista_presenca`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_lista_presenca`  AS SELECT `a`.`id_aluno` AS `id_aluno`, `a`.`nome` AS `nome`, `d`.`nome` AS `disciplina` FROM ((`aluno` `a` join `registro_frequencia` `f` on(`a`.`id_aluno` = `f`.`id_aluno`)) join `disciplina` `d` on(`f`.`id_disciplina` = `d`.`id_disciplina`)) ;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `aluno`
--
ALTER TABLE `aluno`
  ADD PRIMARY KEY (`id_aluno`),
  ADD KEY `idx_aluno_nome` (`nome`);

--
-- Índices de tabela `avaliacao`
--
ALTER TABLE `avaliacao`
  ADD PRIMARY KEY (`id_boletim`),
  ADD KEY `fk_avaliacao_aluno` (`id_aluno`),
  ADD KEY `fk_avaliacao_disciplina` (`id_disciplina`),
  ADD KEY `idx_avaliacao_data` (`id_disciplina`,`data_avaliacao`);

--
-- Índices de tabela `disciplina`
--
ALTER TABLE `disciplina`
  ADD PRIMARY KEY (`id_disciplina`);

--
-- Índices de tabela `disciplina_professor`
--
ALTER TABLE `disciplina_professor`
  ADD PRIMARY KEY (`id_professor`,`id_disciplina`),
  ADD KEY `fk_dp_disciplina` (`id_disciplina`);

--
-- Índices de tabela `especialidade_professor`
--
ALTER TABLE `especialidade_professor`
  ADD PRIMARY KEY (`id_especialidade`);

--
-- Índices de tabela `matricula_disciplina`
--
ALTER TABLE `matricula_disciplina`
  ADD PRIMARY KEY (`id_aluno`,`id_disciplina`,`id_turma`),
  ADD KEY `fk_md_disciplina` (`id_disciplina`),
  ADD KEY `fk_md_turma` (`id_turma`);

--
-- Índices de tabela `periodo_ferias`
--
ALTER TABLE `periodo_ferias`
  ADD PRIMARY KEY (`id_ferias`),
  ADD KEY `fk_ferias_periodo` (`id_periodo`);

--
-- Índices de tabela `periodo_letivo`
--
ALTER TABLE `periodo_letivo`
  ADD PRIMARY KEY (`id_periodo`);

--
-- Índices de tabela `professor`
--
ALTER TABLE `professor`
  ADD PRIMARY KEY (`id_professor`),
  ADD KEY `fk_professor_especialidade` (`id_especialidade`),
  ADD KEY `idx_professor_nome` (`nome`);

--
-- Índices de tabela `registro_frequencia`
--
ALTER TABLE `registro_frequencia`
  ADD PRIMARY KEY (`id_frequencia`),
  ADD KEY `fk_frequencia_aluno` (`id_aluno`),
  ADD KEY `fk_frequencia_disciplina` (`id_disciplina`),
  ADD KEY `idx_frequencia_busca` (`id_disciplina`,`data_aula`,`status_presenca`);

--
-- Índices de tabela `resultado_final`
--
ALTER TABLE `resultado_final`
  ADD PRIMARY KEY (`id_aluno`,`id_disciplina`),
  ADD KEY `fk_resultado_disciplina` (`id_disciplina`);

--
-- Índices de tabela `turma`
--
ALTER TABLE `turma`
  ADD PRIMARY KEY (`id_turma`),
  ADD KEY `fk_turma_periodo` (`id_periodo`);

--
-- Índices de tabela `turma_disciplina`
--
ALTER TABLE `turma_disciplina`
  ADD PRIMARY KEY (`id_turma`,`id_disciplina`,`id_professor`),
  ADD KEY `fk_td_disciplina` (`id_disciplina`),
  ADD KEY `fk_td_professor` (`id_professor`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `aluno`
--
ALTER TABLE `aluno`
  MODIFY `id_aluno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `avaliacao`
--
ALTER TABLE `avaliacao`
  MODIFY `id_boletim` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `disciplina`
--
ALTER TABLE `disciplina`
  MODIFY `id_disciplina` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `especialidade_professor`
--
ALTER TABLE `especialidade_professor`
  MODIFY `id_especialidade` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `periodo_ferias`
--
ALTER TABLE `periodo_ferias`
  MODIFY `id_ferias` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `periodo_letivo`
--
ALTER TABLE `periodo_letivo`
  MODIFY `id_periodo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `professor`
--
ALTER TABLE `professor`
  MODIFY `id_professor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `registro_frequencia`
--
ALTER TABLE `registro_frequencia`
  MODIFY `id_frequencia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `turma`
--
ALTER TABLE `turma`
  MODIFY `id_turma` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `avaliacao`
--
ALTER TABLE `avaliacao`
  ADD CONSTRAINT `fk_avaliacao_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_avaliacao_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`) ON DELETE CASCADE;

--
-- Restrições para tabelas `disciplina_professor`
--
ALTER TABLE `disciplina_professor`
  ADD CONSTRAINT `fk_dp_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_dp_professor` FOREIGN KEY (`id_professor`) REFERENCES `professor` (`id_professor`) ON DELETE CASCADE;

--
-- Restrições para tabelas `matricula_disciplina`
--
ALTER TABLE `matricula_disciplina`
  ADD CONSTRAINT `fk_md_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_md_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_md_turma` FOREIGN KEY (`id_turma`) REFERENCES `turma` (`id_turma`) ON DELETE CASCADE;

--
-- Restrições para tabelas `periodo_ferias`
--
ALTER TABLE `periodo_ferias`
  ADD CONSTRAINT `fk_ferias_periodo` FOREIGN KEY (`id_periodo`) REFERENCES `periodo_letivo` (`id_periodo`) ON DELETE CASCADE;

--
-- Restrições para tabelas `professor`
--
ALTER TABLE `professor`
  ADD CONSTRAINT `fk_professor_especialidade` FOREIGN KEY (`id_especialidade`) REFERENCES `especialidade_professor` (`id_especialidade`) ON DELETE CASCADE;

--
-- Restrições para tabelas `registro_frequencia`
--
ALTER TABLE `registro_frequencia`
  ADD CONSTRAINT `fk_frequencia_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_frequencia_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`) ON DELETE CASCADE;

--
-- Restrições para tabelas `resultado_final`
--
ALTER TABLE `resultado_final`
  ADD CONSTRAINT `fk_resultado_aluno` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_resultado_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`) ON DELETE CASCADE;

--
-- Restrições para tabelas `turma`
--
ALTER TABLE `turma`
  ADD CONSTRAINT `fk_turma_periodo` FOREIGN KEY (`id_periodo`) REFERENCES `periodo_letivo` (`id_periodo`) ON DELETE CASCADE;

--
-- Restrições para tabelas `turma_disciplina`
--
ALTER TABLE `turma_disciplina`
  ADD CONSTRAINT `fk_td_disciplina` FOREIGN KEY (`id_disciplina`) REFERENCES `disciplina` (`id_disciplina`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_td_professor` FOREIGN KEY (`id_professor`) REFERENCES `professor` (`id_professor`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_td_turma` FOREIGN KEY (`id_turma`) REFERENCES `turma` (`id_turma`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
