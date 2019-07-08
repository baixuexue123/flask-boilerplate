CREATE TABLE `user`
(
    `id`           INT          NOT NULL AUTO_INCREMENT,
    `username`     VARCHAR(30)  NOT NULL COMMENT '域账号',
    `password`     VARCHAR(128) NOT NULL,
    `name`         VARCHAR(20)  NOT NULL,
    `email`        VARCHAR(50)  NOT NULL,

    `is_superuser` TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '超级用户',
    `is_stuff`     TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '登录管理后台',
    `is_active`    TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '激活',

    `create_ts`    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `change_ts`    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY (`username`)
) ENGINE = INNODB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8
  COLLATE = utf8_bin COMMENT = '用户';


CREATE TABLE `group`
(
    `id`   INT          NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(30)  NOT NULL,
    `memo` VARCHAR(200) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    UNIQUE KEY (`name`)
) ENGINE = INNODB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = UTF8
  COLLATE = utf8_bin COMMENT = '组';


CREATE TABLE `user_groups`
(
    `id`       INT NOT NULL AUTO_INCREMENT,
    `user_id`  INT NOT NULL,
    `group_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`group_id`) REFERENCES `group` (`id`) ON DELETE CASCADE,
    UNIQUE KEY (`user_id`, `group_id`)
) ENGINE = INNODB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = UTF8
  COLLATE = utf8_bin COMMENT = '用户与组的关系';


CREATE TABLE `permission`
(
    `id`   INT          NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50)  NOT NULL,
    `memo` VARCHAR(200) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    UNIQUE KEY (`name`)
) ENGINE = INNODB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = UTF8
  COLLATE = utf8_bin COMMENT = '权限';


CREATE TABLE `user_permissions`
(
    `id`            INT NOT NULL AUTO_INCREMENT,
    `user_id`       INT NOT NULL,
    `permission_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE CASCADE,
    UNIQUE KEY (`user_id`, `permission_id`)
) ENGINE = INNODB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = UTF8
  COLLATE = utf8_bin COMMENT = '用户权限';


CREATE TABLE `group_permissions`
(
    `id`            INT NOT NULL AUTO_INCREMENT,
    `group_id`      INT NOT NULL,
    `permission_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`group_id`) REFERENCES `group` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE CASCADE,
    UNIQUE KEY (`group_id`, `permission_id`)
) ENGINE = INNODB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = UTF8
  COLLATE = utf8_bin COMMENT = '组权限';
