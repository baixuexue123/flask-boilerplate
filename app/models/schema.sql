-- -------------------------------------------------------------
-- 用户管理
-- -------------------------------------------------------------

CREATE TABLE `user`
(
    `id`           INT          NOT NULL AUTO_INCREMENT COMMENT '主键',
    `username`     VARCHAR(30)  NOT NULL COMMENT '域账号',
    `password`     VARCHAR(128) NOT NULL COMMENT '密码',
    `name`         VARCHAR(20)  NOT NULL COMMENT '姓名',
    `email`        VARCHAR(50)  NOT NULL COMMENT '邮箱',

    `is_superuser` TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '超级用户',
    `is_stuff`     TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '登录管理后台',
    `is_active`    TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '激活',

    `create_ts`    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `change_ts`    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_username` (`username`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_bin COMMENT ='用户';


CREATE TABLE `group`
(
    `id`   INT          NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name` VARCHAR(30)  NOT NULL COMMENT '名称',
    `memo` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_name` (`name`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_bin COMMENT ='用户组';


CREATE TABLE `user_groups`
(
    `id`       INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `user_id`  INT NOT NULL COMMENT '用户id',
    `group_id` INT NOT NULL COMMENT '组id',
    PRIMARY KEY (`id`),
    KEY `idx_group_id` (`group_id`),
    UNIQUE KEY `idx_user_group` (`user_id`, `group_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_bin COMMENT ='用户与组的关系';


CREATE TABLE `permission`
(
    `id`   INT          NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name` VARCHAR(50)  NOT NULL COMMENT '名称',
    `memo` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_bin COMMENT ='权限';


CREATE TABLE `user_permissions`
(
    `id`            INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `user_id`       INT NOT NULL COMMENT '用户id',
    `permission_id` INT NOT NULL COMMENT '权限id',
    PRIMARY KEY (`id`),
    KEY `idx_permission_id` (`permission_id`),
    UNIQUE KEY `idx_user_permission` (`user_id`, `permission_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_bin COMMENT ='用户权限';


CREATE TABLE `group_permissions`
(
    `id`            INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `group_id`      INT NOT NULL COMMENT '组id',
    `permission_id` INT NOT NULL COMMENT '权限id',
    PRIMARY KEY (`id`),
    KEY `idx_permission_id` (`permission_id`),
    UNIQUE KEY `idx_group_id_permission_id` (`group_id`, `permission_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_bin COMMENT ='组与权限的关系';