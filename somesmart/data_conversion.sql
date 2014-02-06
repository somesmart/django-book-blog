-- insert into mission_books.author_lookup
select @curRow := @curRow + 1 AS id
	  ,last_name
	  ,first_name
	  ,birth_date
	  ,death_date
	  ,pen_name
	  ,parent_author
	from (select distinct authorlst as last_name, authorfst as first_name, null birth_date, null death_date, 0 pen_name, 0 parent_author 
			FROM mission_books.bookmaster order by last_name, first_name) authors
JOIN (SELECT @curRow := 0) r;

-- INSERT INTO `mission_django`.`somesmart_author`
-- (`birth_date`,
-- `death_date`,
-- `first_name`,
-- `id`,
-- `last_name`,
-- `parent_author_id`,
-- `pen_name`)
select birth_date, death_date, first_name, id, last_name, NULL parent_author, pen_name from mission_books.author_lookup;

-- insert mission_books.genres
select @curRow := @curRow + 1 AS id
	  ,genre
	from (select distinct genre 
			FROM mission_books.bookmaster order by genre) genres
JOIN (SELECT @curRow := 0) r;

-- insert into mission_django.somesmart_genre
-- (id,
-- name)
select id, genre from mission_books.genres;

-- INSERT INTO `mission_django`.`somesmart_book`
-- (`author_id`,
-- `content_advisory`,
-- `genre_id`,
-- `id`,
-- `original_publication`,
-- `reading_age`,
-- `synopsis`,
-- `title`)
select author_lookup.id
	  ,rdg_age.whyage
      ,genres.id
      ,isbn_lookup.id
      ,NULL original_publication
      ,rdg_age.rdgage
      ,rdg_age.synopsis
      ,title
from mission_books.bookmaster
inner join mission_books.isbn_lookup
on isbn_lookup.isbn = bookmaster.bookid
inner join mission_books.author_lookup
on author_lookup.last_name = bookmaster.authorlst
and author_lookup.first_name = bookmaster.authorfst
inner join mission_books.genres
on genres.genre = bookmaster.genre
left outer join (SELECT distinct
`booksread`.`bookid`,
`booksread`.`rdgage`,
`booksread`.`whyage`,
replace(synopsis, '<br>', '') as synopsis
FROM `mission_books`.`booksread`
order by bookid) rdg_age
on rdg_age.bookid = isbn_lookup.isbn;

-- INSERT INTO `mission_django`.`somesmart_edition`
-- (`book_id`,
-- `cover`,
-- `format`,
-- `isbn`,
-- `pages`,
-- `published`)
select isbn_lookup.id book_id, '' cover, 
case format when 'hardcover' then 1 when 'paperback' then 2 when 'eBook' then 3 when 'audio' then 4 end format,
bookid,
pages,
publishdate
from mission_books.bookmaster
inner join mission_books.isbn_lookup
on isbn_lookup.isbn = bookmaster.bookid;

-- INSERT INTO `mission_django`.`somesmart_review`
--(`reader_id`,
-- `started`,
-- `finished`,
-- `edition_id`,
-- `critique`,
-- `one_sentence`,
-- `recommend`) 
select 2 as reader_id
	  ,startread
	  ,finishread
	  ,somesmart_edition.id as edition_id
	  ,replace(replace(replace(critique,'<br>',''),'<br />',''),'â€™','''')critique
	  ,'' one_sentence
	  ,case when recommend = 'y' then 1 else 0 end recommend
from mission_books.booksread
left outer join mission_django.somesmart_edition
on somesmart_edition.isbn = booksread.bookid

-- INSERT INTO `somesmart_quotetype`(`id`, `name`) 
VALUES (1, 'Favorite'), (2, 'First Line'), (3, 'Last Line'), (4, 'Note')

--INSERT INTO `somesmart_quote`
--(`edition_id`,
-- `reader_id`,
-- `quote_type_id`,
-- `quote`,
-- `page`)
select somesmart_edition.id as edition_id
	  ,2 as reader_id
	  ,quotetypeid as quote_type_id
	  ,quote
	  ,pageno as page
from mission_books.quotes
inner join mission_django.somesmart_edition
on somesmart_edition.isbn = quotes.bookid

-- INSERT INTO `somesmart_radar`
-- (`book_id`,
-- `maturity`,
-- `violence`,
-- `action`,
-- `epic`,
-- `world`,
-- `realism`,
-- `modernity`,
-- `humor`)
select isbn_lookup.id as book_id
	  ,maturity
	  ,violence
	  ,action
	  ,epic
	  ,world
	  ,realism
	  ,modernity
	  ,humor
from mission_books.radars
inner join mission_books.isbn_lookup
on isbn_lookup.isbn = radars.bookid


--some data cleanup:

SELECT title, 
replace(
	replace(
		replace(
			replace(
				replace(synopsis,'â€œ','"')
				,'â€“','-')
		,'â€™','''')
	,'â€˜','"')
,'â€','"') synopsis FROM `somesmart_book` where synopsis != ''

update mission_django.somesmart_review
set critique = replace(
	replace(
		replace(
			replace(
				replace(critique,'â€œ','"')
				,'â€“','-')
		,'â€™','''')
	,'â€˜','"')
,'â€','"')
where critique != ''


-- converting wp2zinnia

-- get category list
SELECT distinct term_taxonomy_id category_id, name category, slug categoryslug FROM `wp_term_relationships` inner join wp_terms on wp_terms.term_id = term_taxonomy_id
inner join wp_posts on wp_posts.ID = object_id
where post_status = 'publish' and post_type = 'post'
order by category_id;

-- select all posts from zinnia
select `id`, `title`, `image`, `content`, `excerpt`, `tags`, `slug`, `status`, `featured`, `comment_enabled`,
`pingback_enabled`, `creation_date`, `last_update`, `start_publication`, `end_publication`, `login_required`, 
`password`, `template` FROM `zinnia_entry`;

SELECT * FROM `wp_posts` where post_status='publish' and post_type = 'post';

-- get categories with post_id
SELECT ID post_id, name category, slug categoryslug FROM `wp_term_relationships` inner join wp_terms on wp_terms.term_id = term_taxonomy_id
inner join wp_posts on wp_posts.ID = object_id
where post_status = 'publish' and post_type = 'post';

-- zinnia_category table probably going to need to set the cats up first
SELECT distinct term_taxonomy_id category_id, name title, slug, '' description, null parent_id, 1 lft, 2 rght, 
0 tree_id, 0 level FROM `wp_term_relationships` inner join wp_terms on wp_terms.term_id = term_taxonomy_id
inner join wp_posts on wp_posts.ID = object_id
where post_status = 'publish' and post_type = 'post'
order by category_id;

-- zinnia_entry table
--insert mission_django.zinnia_entry
SELECT distinct wp_posts.`ID` as id, `post_title` as title, '' image, post_content content, `post_excerpt` as excerpt,
'' tags, post_name as slug, 2 as status, 0 as featured, 1 as comment_enabled, 1 as pingback_enabled,`post_date` creation_date,
`post_modified` as last_update, 'post_date' start_publication, '2042-03-15' end_publication, 0 login_required, '' password,
'zinnia/entry_detail.html' template, case when wp_posts.id = 560 then 122 when wp_posts.id = 777 then 123 else somesmart_book.id end book_id 
FROM `wp_posts` 
left outer join mission_django.somesmart_book
on somesmart_book.title like concat('%',post_title,'%') COLLATE utf8_unicode_ci
where post_status='publish' and post_type = 'post' and wp_posts.id not in (1,5,12,17,19,48)
order by post_title

--second batch of posts I forgot to import the first time:
SELECT distinct wp_posts.`ID` as id, `post_title` as title, '' image, post_content content, `post_excerpt` as excerpt,
'' tags, post_name as slug, 2 as status, 0 as featured, 1 as comment_enabled, 1 as pingback_enabled,`post_date` creation_date,
`post_modified` as last_update, post_date start_publication, '2042-03-15' end_publication, 0 login_required, '' password,
'zinnia/entry_detail.html' template, case when wp_posts.id = 560 then 122 when wp_posts.id = 777 then 123 else somesmart_book.id end book_id 
FROM `wp_posts` 
left outer join mission_django.somesmart_book
on post_title like concat('%',somesmart_book.title,'%') COLLATE utf8_unicode_ci
where post_status = 'publish' and post_type = 'post' and wp_posts.ID not in (select id from mission_django.zinnia_entry) and wp_posts.id not in (3,12,17,19,48)

-- zinnia_entry_authors
--insert zinnia_entry_authors
select @curRow := @curRow + 1 AS id
      ,entry_id
      ,user_id
      FROM (select zinnia_entry.id as entry_id, 2 as user_id
from zinnia_entry where zinnia_entry.id not in (select distinct entry_id from zinnia_entry_authors)) authors
      JOIN (SELECT @curRow := 17) r;

-- zinnia_entry_categories
select @curRow := @curRow + 1 AS id
      ,entry_id
      ,category_id
      FROM (select zinnia_entry.id as entry_id, 4 as category_id
from zinnia_entry where zinnia_entry.id not in (select distinct entry_id from zinnia_entry_categories)) categories
      JOIN (SELECT @curRow := 36) r;


-- zinnia_entry_sites
select @curRow := @curRow + 1 AS id
      ,entry_id
      ,site_id
      FROM (select zinnia_entry.id as entry_id, 2 as site_id
from zinnia_entry where zinnia_entry.id not in (select distinct entry_id from zinnia_entry_sites)) sites
      JOIN (SELECT @curRow := 17) r;

--some data cleanup
update `zinnia_entry` 
set content = replace(replace(content,'<em>','*'),'</em>','*')
where content like '%<em>%'

--bringing over comments
--look into using https://github.com/HonzaKral/django-threadedcomments
SELECT * FROM mission_wdps3.`wp_comments`where comment_type != 'pingback' and comment_approved = 1
SELECT `id`
     ,`content_type_id`
     ,`object_pk`
     ,`site_id`
     ,`user_id`
     ,`user_name`
     ,`user_email`
     ,`user_url`
     ,`comment`
     ,`submit_date`
     ,`ip_address`
     ,`is_public`
     ,`is_removed` 
     FROM `django_comments` WHERE


SELECT @curRow := @curRow + 1 AS id
	,content_type_id
	,object_pk
	,site_id
	,user_id
	,user_name
	,user_email
	,user_url
	,comment
	,submit_date
	,ip_address
	,is_public
	,is_removed
FROM (select 49 content_type_id
      ,zinnia_entry.id object_pk
      ,2 site_id
      ,case when comment_author_email='sf1179@gmail.com' then 2 else NULL end user_id
      ,comment_author user_name
      ,comment_author_email user_email
      ,comment_author_url user_url
      ,comment_content comment
      ,comment_date submit_date
      ,comment_author_ip ip_address
      ,1 is_public
      ,0 is_removed
FROM mission_wdps3.`wp_comments`
left outer join mission_wdps3.wp_posts
on wp_posts.ID = wp_comments.comment_post_id
left outer join mission_django.zinnia_entry
on zinnia_entry.title = wp_posts.post_title COLLATE utf8_unicode_ci
where comment_type != 'pingback' and comment_approved = 1
and comment_id not in (20)) comments
JOIN (SELECT @curRow := 9) r;


SELECT `id`
     ,`content_type_id`
     ,`object_pk`
     ,`site_id`
     ,`user_id`
     ,`user_name`
     ,`user_email`
     ,`user_url`
     ,`comment`
     ,`submit_date`
     ,`ip_address`
     ,`is_public`
     ,`is_removed` 
FROM `django_comments` 
left outer join (SELECT wp_comments.comment_ID as old_id
      ,django_comments.id as new_id
FROM  mission_wdps3.`wp_comments` 
INNER JOIN mission_django.django_comments 
ON django_comments.comment = comment_content COLLATE utf8_unicode_ci) cmt_lookup
on cmt_lookup.new_id = django_comments.id