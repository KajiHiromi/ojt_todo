INSERT INTO user (
  name,
  password
)
VALUES (
  "kaji",
  "kaji"
);

INSERT INTO tag (
  tag
)
VALUES (
  "プライベート"
),
(
  "ビジネス"
);

INSERT INTO task (
  name,
  limit_time,
  memo,
  user_id
) 
VALUES (
  "プレゼン資料",
  "2013-06-25 12:00:00",
  "aaaaaaaa",
  1  
);

INSERT INTO task (
  name,
  limit_time,
  memo,
  user_id
)
VALUES (
  "共有会資料",
  "2013-06-26 12:00",
  "bbbbbbb",
  1
);

INSERT INTO task (
  name,
  limit_time,
  memo,
  user_id
)
VALUES (
  "ランチ予約",
  "2013-06-30 12:00",
  "ccccccccc",
  1
);


INSERT INTO tasktag (
  task_id,
  tag_id
)
VALUES (
  1,
  1
),
(
  2,
  1
),
(
  3,
  2
);











