import java.awt.RenderingHints.Key;
import java.io.*;
import java.security.KeyStore.Entry;
import java.text.Normalizer;
import java.util.*;

public class new493 {

	public static void main(String[] args) throws IOException {
		BufferedReader select = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("Please write the number of selection.\n1.Ignore Stop Words\n2.Calculate With Stop Words");
		String selection = select.readLine();
		getText();
		Map<String, String> tokensWithIndexes;
		Map<String, String> inverseIndexMap;
		if(selection.equals("2")){
			tokensWithIndexes = tokenizer();
			inverseIndexMap = inverseIndex(tokensWithIndexes);
			mostCommons(tokensWithIndexes);
			boolOperation(inverseIndexMap );

		}else if(selection.equals("1")){
			tokensWithIndexes = tokenizerWithoutStopwords();
			inverseIndexMap = inverseIndex(tokensWithIndexes);
			mostCommons(tokensWithIndexes);
			boolOperation(inverseIndexMap );

		}else{
			System.out.println("Wrong selection, please restart and try again.");
		}
	}

	public static void boolOperation(Map<String, String> inverseIndexMap) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("Enter number for the operation\n1.AND\n2.OR");
		String operation = br.readLine();
		System.out.println("How many words do you want to search?");
		int operationCount = Integer.parseInt(br.readLine());
		String[] words = new String[operationCount];
		String[] indexes = new String[operationCount];
		Stemmer stem = new Stemmer();
		String input = "";
		for (int i = 0; i < operationCount; i++) {
			System.out.println("Enter word number " + i + ":");
			input = br.readLine();
			stem.add(input.toCharArray(), input.length());
			stem.stem();
			words[i] = stem.toString();
		}
		br.close();
		for (int j = 0; j < operationCount; j++) {
			indexes[j] = inverseIndexMap.get(words[j]);
		}
		if (operation == "1") {
			List<Integer> commonLocations = new ArrayList<Integer>();
			if (indexes[0].contains(",")) {
				commonLocations.add(Integer.parseInt(indexes[0].substring(0, indexes[0].indexOf(","))));
				indexes[0] = indexes[0].substring(indexes[0].indexOf(",") + 1);
				while (indexes[0].contains(",")) {
					commonLocations.add(Integer.parseInt(indexes[0].substring(0, indexes[0].indexOf(","))));
					indexes[0] = indexes[0].substring(indexes[0].indexOf(",") + 1);
				}

			} else {
				commonLocations.add(Integer.parseInt(indexes[0]));
			}

			for (int k = 1; k < operationCount; k++) {
				List<Integer> locations = new ArrayList<Integer>();
				List<Integer> tempLocations = new ArrayList<Integer>();
				if (indexes[k].contains(",")) {
					locations.add(Integer.parseInt(indexes[k].substring(0, indexes[k].indexOf(","))));
					indexes[k] = indexes[k].substring(indexes[k].indexOf(",") + 1);
					while (indexes[k].contains(",")) {
						locations.add(Integer.parseInt(indexes[k].substring(0, indexes[k].indexOf(","))));
						indexes[k] = indexes[k].substring(indexes[k].indexOf(",") + 1);
					}

				} else {
					locations.add(Integer.parseInt(indexes[k]));
				}
				for (Integer val : locations) {
					if (commonLocations.contains(val)) {
						tempLocations.add(val);
					}
				}
				commonLocations.clear();
				commonLocations = tempLocations;

			}
			System.out.println("The files that contains all of keywords :");
			if (commonLocations.size() > 0) {
				System.out.print(commonLocations.get(0));

				for (int i = 1; i < commonLocations.size(); i++) {
					System.out.print(", " + commonLocations.get(i));
				}
			}
		} else if (operation == "2") {
			List<Integer> commonLocations = new ArrayList<Integer>();
			if (indexes[0].contains(",")) {
				commonLocations.add(Integer.parseInt(indexes[0].substring(0, indexes[0].indexOf(","))));
				indexes[0] = indexes[0].substring(indexes[0].indexOf(",") + 1);
				while (indexes[0].contains(",")) {
					commonLocations.add(Integer.parseInt(indexes[0].substring(0, indexes[0].indexOf(","))));
					indexes[0] = indexes[0].substring(indexes[0].indexOf(",") + 1);
				}

			} else {
				commonLocations.add(Integer.parseInt(indexes[0]));
			}

			for (int k = 1; k < operationCount; k++) {
				List<Integer> locations = new ArrayList<Integer>();
				List<Integer> tempLocations = new ArrayList<Integer>();
				if (indexes[k].contains(",")) {
					locations.add(Integer.parseInt(indexes[k].substring(0, indexes[k].indexOf(","))));
					indexes[k] = indexes[k].substring(indexes[k].indexOf(",") + 1);
					while (indexes[k].contains(",")) {
						locations.add(Integer.parseInt(indexes[k].substring(0, indexes[k].indexOf(","))));
						indexes[k] = indexes[k].substring(indexes[k].indexOf(",") + 1);
					}

				} else {
					locations.add(Integer.parseInt(indexes[k]));
				}
				for (Integer val : locations) {
					if (!commonLocations.contains(val)) {
						tempLocations.add(val);
					}
				}
				commonLocations.addAll(tempLocations);

			}
			System.out.println("The files that contains at least one of keywords :");
			Collections.sort(commonLocations);
			System.out.print(commonLocations.get(0));

			for (int i = 1; i < commonLocations.size(); i++) {
				System.out.print(", " + commonLocations.get(i));
			}
		}

	}

	public static void mostCommons(Map<String, String> tokens) throws IOException {
		Map<String, Integer> mostCommon = new HashMap<String, Integer>();

		for (Map.Entry<String, String> e : tokens.entrySet()) {

			int count = 0;
			String value = e.getValue();
			count++;
			value = value.substring(value.indexOf(">") + 1);
			while (value.contains(">")) {
				count++;
				value = value.substring(value.indexOf(">") + 1);
			}
			mostCommon.put(e.getKey(), count);

		}

		mostCommon = sortByValues(mostCommon);
		PrintWriter tokenfile = new PrintWriter("MostCommon.txt", "UTF-8");
		
		for (Map.Entry<String, Integer> e : mostCommon.entrySet()) {
			tokenfile.println(e.getKey() + "=" + e.getValue());
		}
		tokenfile.close();
	}
	
	  
	
	
private static Map<String, Integer> sortByValues(Map<String, Integer> tokens) { 
    List<Map.Entry<String, Integer>> list = new LinkedList(tokens.entrySet());
    // Defined Custom Comparator here
    Collections.sort(list, new Comparator() {
         public int compare(Object o1, Object o2) {
            return ((Comparable) ((Map.Entry) (o1)).getValue())
               .compareTo(((Map.Entry) (o2)).getValue());
         }
    });

    // Here I am copying the sorted list in HashMap
    // using LinkedHashMap to preserve the insertion order
    Map<String,Integer> sortedHashMap = new LinkedHashMap<String,Integer>();
    for (Iterator it = list.iterator(); it.hasNext();) {
           Map.Entry entry = (Map.Entry) it.next();
           sortedHashMap.put(entry.getKey().toString(), Integer.parseInt(entry.getValue().toString()));
    } 
    return sortedHashMap;
}

	public static Map<String, String> inverseIndex(Map<String, String> tokens) throws IOException {
		Map<String, String> inverseIndexMap = new HashMap<String, String>();

		for (Map.Entry<String, String> e : tokens.entrySet()) {

			String indexes = "";
			String value = e.getValue();
			indexes = value.substring(0, value.indexOf(">"));
			value = value.substring(value.indexOf(">") + 1);
			while (value.contains(">")) {
				if (!indexes.contains(value.substring(value.indexOf("|") + 1, value.indexOf(">")))) {
					indexes = indexes + "," + value.substring(value.indexOf("|") + 1, value.indexOf(">"));
				}
				value = value.substring(value.indexOf(">") + 1);
			}
			inverseIndexMap.put(e.getKey(), indexes);

		}

		PrintWriter tokenfile = new PrintWriter("tokens.txt", "UTF-8");
		for (Map.Entry<String, String> e : inverseIndexMap.entrySet()) {
			tokenfile.println(e.getKey() + "=" + e.getValue());
		}
		tokenfile.close();
		return inverseIndexMap;
	}

	public static Map<String, String> tokenizer() throws IOException {
		Map<String, String> tokens = new HashMap<String, String>();
		int total = 0;
		int indexOfNews = 0;
		for (int fileCount = 0; fileCount < 22; fileCount++) {
			BufferedReader br = new BufferedReader(new FileReader("bodies" + fileCount + ".txt"));
			StringBuilder sb = new StringBuilder();
			String line = br.readLine();

			while (line != null) {
				sb.append(line);
				sb.append(System.lineSeparator());
				line = br.readLine();
			}
			String everything = sb.toString();

			br.close();

			Stemmer ad = new Stemmer();
			while (everything.contains("IndexOfNews=")) {
				String oneNews = everything.substring((everything.indexOf("IndexOfNews=") + 13),
						(everything.indexOf("EndOfNews")));
				indexOfNews++;
				String token = "";
				oneNews = oneNews.replaceAll("[.,']", "");
				oneNews = oneNews.replaceAll("[!?><)(;:\n\t\"]", " ");
				StringTokenizer tokenizeText = new StringTokenizer(oneNews, " ");
				total += tokenizeText.countTokens();
				int place = 0;
				String key = "";
				while (tokenizeText.hasMoreElements()) {
					token = tokenizeText.nextElement().toString();
					key = indexOfNews + ">" + place;
					ad.add(token.toCharArray(), token.length());
					ad.stem();
					if (tokens.containsKey(ad.toString())) {
						tokens.replace(ad.toString(), tokens.get(ad.toString()), tokens.get(ad.toString()) + "|" + key);
					} else {
						tokens.put(ad.toString(), key);
					}
					place++;
				}

				everything = everything.substring(everything.indexOf("EndOfNews") + 9);
			}
		}
		Map<String, String> treeMap = new TreeMap<String, String>(tokens);
		System.out.println("Total Number Of Tokens = " + total);
		System.out.println("Total Number of Terms = " + treeMap.size());
		return treeMap;
	}
	public static Map<String, String> tokenizerWithoutStopwords() throws IOException {
		Map<String, String> tokens = new HashMap<String, String>();
		List<String> stopWords = new ArrayList<String>();
		
		stopWords.add("a");
		stopWords.add("an");
		stopWords.add("all");
		stopWords.add("and");
		stopWords.add("any");
		stopWords.add("are");
		stopWords.add("as");
		stopWords.add("be");
		stopWords.add("been");
		stopWords.add("but");
		stopWords.add("by");
		stopWords.add("few");
		stopWords.add("for");
		stopWords.add("have");
		stopWords.add("he");
		stopWords.add("her");
		stopWords.add("here");
		stopWords.add("him");
		stopWords.add("his");
		stopWords.add("how");
		stopWords.add("i");
		stopWords.add("in");
		stopWords.add("is");
		stopWords.add("it");
		stopWords.add("its");
		stopWords.add("many");
		stopWords.add("me");
		stopWords.add("my");
		stopWords.add("none");
		stopWords.add("of");
		stopWords.add("on");
		stopWords.add("or");
		stopWords.add("our");
		stopWords.add("she");
		stopWords.add("some");
		stopWords.add("the");
		stopWords.add("their");
		stopWords.add("them");
		stopWords.add("they");
		stopWords.add("there");
		stopWords.add("that");
		stopWords.add("this");
		stopWords.add("us");
		stopWords.add("was");
		stopWords.add("what");
		stopWords.add("when");
		stopWords.add("where");
		stopWords.add("which");
		stopWords.add("who");
		stopWords.add("why");
		stopWords.add("will");
		stopWords.add("with");
		stopWords.add("you");
		stopWords.add("your");
		
		
		int total = 0;
		int indexOfNews = 0;
		for (int fileCount = 0; fileCount < 22; fileCount++) {
			BufferedReader br = new BufferedReader(new FileReader("bodies" + fileCount + ".txt"));
			StringBuilder sb = new StringBuilder();
			String line = br.readLine();

			while (line != null) {
				sb.append(line);
				sb.append(System.lineSeparator());
				line = br.readLine();
			}
			String everything = sb.toString();

			br.close();

			Stemmer ad = new Stemmer();
			while (everything.contains("IndexOfNews=")) {
				String oneNews = everything.substring((everything.indexOf("IndexOfNews=") + 13),
						(everything.indexOf("EndOfNews")));
				indexOfNews++;
				String token = "";
				oneNews = oneNews.replaceAll("[.,']", "");
				
				oneNews = oneNews.replaceAll("[!?><)(;:\n\t\"]", " ");
				StringTokenizer tokenizeText = new StringTokenizer(oneNews, " ");
				total += tokenizeText.countTokens();
				int place = 0;
				String key = "";
				while (tokenizeText.hasMoreElements()) {
					token = tokenizeText.nextElement().toString();
					if(stopWords.contains(token)){
						continue;
					}
					key = indexOfNews + ">" + place;
					ad.add(token.toCharArray(), token.length());
					ad.stem();
					if (tokens.containsKey(ad.toString())) {
						tokens.replace(ad.toString(), tokens.get(ad.toString()), tokens.get(ad.toString()) + "|" + key);
					} else {
						tokens.put(ad.toString(), key);
					}
					place++;
				}

				everything = everything.substring(everything.indexOf("EndOfNews") + 9);
			}
		}
		Map<String, String> treeMap = new TreeMap<String, String>(tokens);
		System.out.println("Total Number Of Tokens = " + total);
		System.out.println("Total Number of Terms = " + treeMap.size());
		return treeMap;
	}

	public static void getText() throws IOException {

		for (int i = 0; i < 22; i++) {
			BufferedReader br;
			if (i < 10) {
				br = new BufferedReader(new FileReader("reuters21578/reut2-00" + i + ".sgm"));
			} else {
				br = new BufferedReader(new FileReader("reuters21578/reut2-0" + i + ".sgm"));
			}
			StringBuilder sb = new StringBuilder();

			String line = br.readLine();

			while (line != null) {
				sb.append(line);
				sb.append(System.lineSeparator());
				line = br.readLine();
			}
			String everything = sb.toString();

			br.close();

			String convertedString = Normalizer.normalize(everything, Normalizer.Form.NFD).replaceAll("[^\\p{ASCII}]",
					"");
			convertedString = convertedString.toLowerCase();
			String s = "";
			PrintWriter writer = new PrintWriter("bodies" + i + ".txt", "UTF-8");
			getBodies(convertedString, s, writer);
			writer.close();
		}

	}
	
	
	
	public static void getBodies(String all, String finalized, PrintWriter output) {
		String title = all.substring(all.indexOf("<TITLE>") + 7, all.indexOf("</TITLE>"));
		finalized = title;
		if (all.substring(0, all.indexOf("&#3;")).contains("<BODY>")) {
			String filtered = all.substring(all.indexOf("<BODY>") + 6, all.indexOf("&#3;</BODY>"));
			finalized += filtered;
		}
		output.println("IndexOfNews=\n" + finalized + "\nEndOfNews\n");
		all = all.substring(all.indexOf("&#3;") + 4);
		if (all.contains("<TITLE>")) {
			all = all.substring(all.indexOf("<TITLE>"));

			getBodies(all, finalized, output);
		}

	}
}
