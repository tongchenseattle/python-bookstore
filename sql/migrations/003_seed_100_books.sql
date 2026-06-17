USE bookstore_local;
GO

SET NOCOUNT ON;

DECLARE @now DATETIME2 = SYSUTCDATETIME();

DECLARE @categories TABLE (
    name NVARCHAR(120) NOT NULL,
    description NVARCHAR(1000) NULL
);

INSERT INTO @categories
    (name, description)
VALUES
    (N'History', N'History titles'),
    (N'Math', N'Mathematics titles'),
    (N'Computer Science', N'Computer science titles');

MERGE dbo.categories AS target
USING @categories AS source
    ON target.name = source.name
WHEN MATCHED THEN
    UPDATE SET
        target.description = source.description,
        target.status = N'active',
        target.updated_at = @now
WHEN NOT MATCHED THEN
    INSERT (id, name, description, status, created_at, updated_at)
    VALUES (NEWID(), source.name, source.description, N'active', @now, @now);

DECLARE @book_seed TABLE (
    category_name NVARCHAR(120) NOT NULL,
    title NVARCHAR(200) NOT NULL,
    publish_date DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description NVARCHAR(4000) NULL
);

INSERT INTO @book_seed
    (category_name, title, publish_date, price, description)
VALUES
    -- History (34)
    (N'History', N'The Histories', '0440-01-01', 14.99, N'Classic history text by Herodotus.'),
    (N'History', N'The History of the Peloponnesian War', '0400-01-01', 15.99, N'Classic history text by Thucydides.'),
    (N'History', N'The Twelve Caesars', '0121-01-01', 13.49, N'Roman imperial biographies by Suetonius.'),
    (N'History', N'The Annals', '0116-01-01', 12.99, N'Roman history by Tacitus.'),
    (N'History', N'The Gallic War', '0058-01-01', 11.99, N'Julius Caesar''s military narrative.'),
    (N'History', N'The Histories (Polybius)', '0146-01-01', 14.49, N'Hellenistic and Roman expansion history.'),
    (N'History', N'SPQR', '2015-01-01', 18.99, N'Ancient Rome by Mary Beard.'),
    (N'History', N'Guns, Germs, and Steel', '1997-01-01', 16.99, N'Global history by Jared Diamond.'),
    (N'History', N'The Silk Roads', '2015-01-01', 17.99, N'History of Eurasian exchange by Peter Frankopan.'),
    (N'History', N'A People''s History of the United States', '1980-01-01', 19.49, N'U.S. social history by Howard Zinn.'),
    (N'History', N'The Rise and Fall of the Third Reich', '1960-01-01', 21.99, N'History of Nazi Germany by William Shirer.'),
    (N'History', N'Team of Rivals', '2005-01-01', 18.49, N'Lincoln and his cabinet by Doris Kearns Goodwin.'),
    (N'History', N'The Diary of a Young Girl', '1947-01-01', 10.99, N'Anne Frank''s wartime diary.'),
    (N'History', N'The Liberation Trilogy', '2013-01-01', 24.99, N'WWII liberation campaign history by Rick Atkinson.'),
    (N'History', N'The Second World War', '2004-01-01', 23.99, N'Comprehensive WWII history by Antony Beevor.'),
    (N'History', N'Postwar', '2005-01-01', 22.99, N'History of Europe after 1945 by Tony Judt.'),
    (N'History', N'The Crusades', '2010-01-01', 17.49, N'Crusader history by Thomas Asbridge.'),
    (N'History', N'Rubicon', '2003-01-01', 16.49, N'Late Roman Republic history by Tom Holland.'),
    (N'History', N'The Sleepwalkers', '2012-01-01', 18.99, N'Origins of World War I by Christopher Clark.'),
    (N'History', N'The Romanovs', '2016-01-01', 20.99, N'Imperial Russian dynasty history by Simon Sebag Montefiore.'),
    (N'History', N'The Plantagenets', '2012-01-01', 18.49, N'Medieval English monarchy history by Dan Jones.'),
    (N'History', N'Grant', '2017-01-01', 21.49, N'Biography of Ulysses S. Grant by Ron Chernow.'),
    (N'History', N'Custer Died for Your Sins', '1969-01-01', 14.99, N'Native American critique by Vine Deloria Jr.'),
    (N'History', N'1776', '2005-01-01', 14.49, N'American Revolution year narrative by David McCullough.'),
    (N'History', N'John Adams', '2001-01-01', 19.99, N'Biography by David McCullough.'),
    (N'History', N'The Warmth of Other Suns', '2010-01-01', 18.99, N'Great Migration history by Isabel Wilkerson.'),
    (N'History', N'The Decline and Fall of the Roman Empire', '1776-01-01', 25.99, N'Classic by Edward Gibbon.'),
    (N'History', N'A Distant Mirror', '1978-01-01', 16.99, N'Fourteenth-century Europe by Barbara Tuchman.'),
    (N'History', N'The Guns of August', '1962-01-01', 15.99, N'Opening of WWI by Barbara Tuchman.'),
    (N'History', N'The First World War', '1998-01-01', 17.99, N'World War I history by John Keegan.'),
    (N'History', N'In the Garden of Beasts', '2011-01-01', 15.49, N'Berlin in the 1930s by Erik Larson.'),
    (N'History', N'The Pity of War', '1998-01-01', 16.49, N'Revisionist WWI study by Niall Ferguson.'),
    (N'History', N'Destiny Disrupted', '2009-01-01', 14.99, N'World history through Islamic civilizations by Tamim Ansary.'),
    (N'History', N'King Leopold''s Ghost', '1998-01-01', 15.99, N'Congo colonial history by Adam Hochschild.'),

    -- Math (33)
    (N'Math', N'Elements', '0300-01-01', 12.99, N'Foundational geometry by Euclid.'),
    (N'Math', N'Disquisitiones Arithmeticae', '1801-01-01', 19.99, N'Number theory by Carl Friedrich Gauss.'),
    (N'Math', N'Concrete Mathematics', '1989-01-01', 27.99, N'Discrete mathematics by Graham, Knuth, and Patashnik.'),
    (N'Math', N'How to Solve It', '1945-01-01', 14.99, N'Problem-solving heuristics by George Polya.'),
    (N'Math', N'A Mathematician''s Apology', '1940-01-01', 11.99, N'Essay by G. H. Hardy.'),
    (N'Math', N'Flatland', '1884-01-01', 9.99, N'Mathematical satire by Edwin A. Abbott.'),
    (N'Math', N'The Joy of x', '2012-01-01', 13.99, N'Accessible math by Steven Strogatz.'),
    (N'Math', N'Infinite Powers', '2019-01-01', 15.99, N'History of calculus by Steven Strogatz.'),
    (N'Math', N'Fermat''s Enigma', '1997-01-01', 14.49, N'Story of Fermat''s Last Theorem by Simon Singh.'),
    (N'Math', N'Prime Obsession', '2003-01-01', 16.49, N'Riemann hypothesis narrative by John Derbyshire.'),
    (N'Math', N'The Man Who Loved Only Numbers', '1998-01-01', 14.99, N'Biography of Paul Erdos by Paul Hoffman.'),
    (N'Math', N'The Music of the Primes', '2003-01-01', 15.49, N'Prime numbers and the Riemann hypothesis by Marcus du Sautoy.'),
    (N'Math', N'What Is Mathematics?', '1941-01-01', 17.99, N'Math overview by Courant and Robbins.'),
    (N'Math', N'Number: The Language of Science', '1930-01-01', 13.49, N'Popular mathematics by Tobias Dantzig.'),
    (N'Math', N'Journey Through Genius', '1990-01-01', 16.99, N'Great mathematical ideas by William Dunham.'),
    (N'Math', N'Mathematics and the Imagination', '1940-01-01', 12.99, N'Math essays by Kasner and Newman.'),
    (N'Math', N'Proofs from THE BOOK', '1998-01-01', 18.49, N'Elegant proofs by Aigner and Ziegler.'),
    (N'Math', N'Calculus', '2007-01-01', 29.99, N'Calculus textbook by James Stewart.'),
    (N'Math', N'Principles of Mathematical Analysis', '1976-01-01', 21.99, N'Analysis textbook by Walter Rudin.'),
    (N'Math', N'Linear Algebra Done Right', '2015-01-01', 20.99, N'Linear algebra text by Sheldon Axler.'),
    (N'Math', N'Algebra', '2002-01-01', 24.99, N'Abstract algebra by Serge Lang.'),
    (N'Math', N'Topology', '2000-01-01', 22.99, N'Topology textbook by James Munkres.'),
    (N'Math', N'A First Course in Probability', '2014-01-01', 23.99, N'Probability text by Sheldon Ross.'),
    (N'Math', N'Probability Theory: The Logic of Science', '2003-01-01', 26.49, N'Bayesian probability by E. T. Jaynes.'),
    (N'Math', N'An Introduction to the Theory of Numbers', '2008-01-01', 24.49, N'Number theory by Hardy and Wright.'),
    (N'Math', N'Visual Complex Analysis', '1997-01-01', 19.49, N'Complex analysis by Tristan Needham.'),
    (N'Math', N'The Princeton Companion to Mathematics', '2008-01-01', 39.99, N'Comprehensive math reference edited by Timothy Gowers.'),
    (N'Math', N'The Art of Problem Solving, Volume 1', '2006-01-01', 27.49, N'Competition-oriented algebra and number theory.'),
    (N'Math', N'Putnam and Beyond', '2006-01-01', 28.99, N'Problem-solving collection by Razvan Gelca and Titu Andreescu.'),
    (N'Math', N'Naive Set Theory', '1960-01-01', 11.49, N'Introductory set theory by Paul Halmos.'),
    (N'Math', N'Gödel, Escher, Bach', '1979-01-01', 18.99, N'Patterns and formal systems by Douglas Hofstadter.'),
    (N'Math', N'Winning Ways for Your Mathematical Plays', '1982-01-01', 34.99, N'Combinatorial game theory by Berlekamp, Conway, and Guy.'),
    (N'Math', N'Introduction to Probability', '2014-01-01', 22.49, N'Probability by Blitzstein and Hwang.'),

    -- Computer Science (33)
    (N'Computer Science', N'Structure and Interpretation of Computer Programs', '1996-01-01', 29.49, N'Classic CS text by Abelson and Sussman.'),
    (N'Computer Science', N'Introduction to Algorithms', '2009-01-01', 44.99, N'CLRS algorithms textbook.'),
    (N'Computer Science', N'Clean Code', '2008-01-01', 31.99, N'Craftsmanship by Robert C. Martin.'),
    (N'Computer Science', N'Design Patterns', '1994-01-01', 39.99, N'GoF object-oriented design patterns.'),
    (N'Computer Science', N'The Pragmatic Programmer', '1999-01-01', 33.99, N'Developer practices by Hunt and Thomas.'),
    (N'Computer Science', N'Code Complete', '2004-01-01', 37.99, N'Software construction by Steve McConnell.'),
    (N'Computer Science', N'Refactoring', '2018-01-01', 42.99, N'Improving existing code by Martin Fowler.'),
    (N'Computer Science', N'Working Effectively with Legacy Code', '2004-01-01', 34.49, N'Legacy code techniques by Michael Feathers.'),
    (N'Computer Science', N'The Mythical Man-Month', '1975-01-01', 24.99, N'Software project essays by Fred Brooks.'),
    (N'Computer Science', N'Computer Networks', '2010-01-01', 49.99, N'Networking by Tanenbaum and Wetherall.'),
    (N'Computer Science', N'Operating System Concepts', '2018-01-01', 54.99, N'Operating systems by Silberschatz, Galvin, and Gagne.'),
    (N'Computer Science', N'Modern Operating Systems', '2014-01-01', 46.99, N'Operating systems by Andrew S. Tanenbaum.'),
    (N'Computer Science', N'Compilers: Principles, Techniques, and Tools', '2006-01-01', 52.99, N'Compiler design by Aho, Lam, Sethi, and Ullman.'),
    (N'Computer Science', N'Database System Concepts', '2010-01-01', 47.99, N'Database fundamentals by Silberschatz, Korth, and Sudarshan.'),
    (N'Computer Science', N'Computer Organization and Design', '2020-01-01', 48.99, N'Computer architecture by Patterson and Hennessy.'),
    (N'Computer Science', N'Computer Architecture: A Quantitative Approach', '2017-01-01', 59.99, N'Advanced architecture by Hennessy and Patterson.'),
    (N'Computer Science', N'Artificial Intelligence: A Modern Approach', '2020-01-01', 56.99, N'AI textbook by Russell and Norvig.'),
    (N'Computer Science', N'Pattern Recognition and Machine Learning', '2006-01-01', 53.99, N'Machine learning by Christopher Bishop.'),
    (N'Computer Science', N'Deep Learning', '2016-01-01', 57.99, N'Deep learning by Goodfellow, Bengio, and Courville.'),
    (N'Computer Science', N'Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow', '2019-01-01', 44.49, N'Applied machine learning by Aurelien Geron.'),
    (N'Computer Science', N'The C Programming Language', '1988-01-01', 28.99, N'C programming by Kernighan and Ritchie.'),
    (N'Computer Science', N'The C++ Programming Language', '2013-01-01', 49.49, N'C++ by Bjarne Stroustrup.'),
    (N'Computer Science', N'Programming Language Pragmatics', '2009-01-01', 41.49, N'Programming language concepts by Michael Scott.'),
    (N'Computer Science', N'Distributed Systems', '2016-01-01', 43.99, N'Distributed systems by Tanenbaum and van Steen.'),
    (N'Computer Science', N'Designing Data-Intensive Applications', '2017-01-01', 38.99, N'Data systems architecture by Martin Kleppmann.'),
    (N'Computer Science', N'Site Reliability Engineering', '2016-01-01', 36.99, N'Google SRE practices.'),
    (N'Computer Science', N'Algorithms', '2011-01-01', 45.49, N'Algorithms by Sedgewick and Wayne.'),
    (N'Computer Science', N'Introduction to the Theory of Computation', '2012-01-01', 46.49, N'Theory of computation by Michael Sipser.'),
    (N'Computer Science', N'The Art of Computer Programming, Volume 1', '1997-01-01', 61.99, N'Fundamental algorithms by Donald Knuth.'),
    (N'Computer Science', N'The Art of Computer Programming, Volume 2', '1998-01-01', 61.99, N'Seminumerical algorithms by Donald Knuth.'),
    (N'Computer Science', N'The Art of Computer Programming, Volume 3', '1998-01-01', 61.99, N'Sorting and searching by Donald Knuth.'),
    (N'Computer Science', N'Computer Systems: A Programmer''s Perspective', '2015-01-01', 47.49, N'Systems programming by Bryant and O''Hallaron.'),
    (N'Computer Science', N'Domain-Driven Design', '2003-01-01', 35.99, N'Software modeling by Eric Evans.');

INSERT INTO dbo.books
    (
    id,
    title,
    publish_date,
    price,
    description,
    status,
    category_id,
    created_at,
    updated_at
    )
SELECT
    NEWID(),
    s.title,
    s.publish_date,
    s.price,
    s.description,
    N'published',
    c.id,
    @now,
    @now
FROM @book_seed AS s
    INNER JOIN dbo.categories AS c
    ON c.name = s.category_name
WHERE NOT EXISTS (
    SELECT 1
FROM dbo.books AS b
    INNER JOIN dbo.categories AS bc
    ON bc.id = b.category_id
WHERE b.title = s.title
    AND bc.name = s.category_name
);

SELECT
    c.name AS category_name,
    COUNT(*) AS seeded_books
FROM dbo.books AS b
    INNER JOIN dbo.categories AS c
    ON c.id = b.category_id
WHERE c.name IN (N'History', N'Math', N'Computer Science')
GROUP BY c.name
ORDER BY c.name;
GO
