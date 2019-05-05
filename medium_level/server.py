"""
API SERVER: MEDIUM LEVEL

This server is going to provide us information about:

(1) List of available species in the ensembl database: you can include a limit, this is, the maximum number of species you
want to see. It's completely optional. You can leave the input in blank in order to see all of them. If the limit exceeds
the number of available species, the maximum number of species will be set as the limit by default.

(2) Karyotype of a given species: if the species is not in the data base, the response will be the error HTML page. On
the other hand, if the species is in the database but the karyotype is not, a message telling that the info is not found
will appear. If the input elements are empty or have wrong type or values, the response will be the error HTML page as well.

(3) Chromosome length of a given species: if the species is not in the data base, the response will be the error HTML page.
On the other hand, if the species is in the database but the chromosome is not, a message telling that the info is not found
will appear. If the input elements are empty or have wrong type or values, the response will be the error HTML page as well.

(4) Gene sequence: it returns the sequence of a given human gene. If the gene is not in the database, the type or the value
of the input is wrong, the response will be the error HTML page.

(5) Gene info: it returns the info of a given human gene (start, end, Length, id and Chromosome where the gene resides).
If the gene is not in the database, the type or the value of the input is wrong, the response will be the error HTML page.

(6) Gene calculations: performs some calculations on the given human gene and returns the total length and the percentage
of all its bases. If the gene is not in the database, the type or the value of the input is wrong, the response will be
the error HTML page.

(7) Chromosome genes: it returns the genes in a specific region of a gene. The input values are: the chromosome, start
and end positions. If the chromosome is not in the database, the type or the value of the input is wrong, the response
will be the error HTML page.

Hope you enjoy :-)


Helena Sofia Yaben

"""
#Import the modules and classes we are going to use
from seq_class import Seq
import http.server
import socketserver
import termcolor
import requests,sys
import json
socketserver.TCPServer.allow_reuse_address = True

# Now we define the server's port
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True



class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Now, we need to know which is the endpoint of the request and depending on it, we will perform different actions
        try:
            if self.path == '/':

                # Open the form1.html file
                f = open("index.html", 'r')
                contents = f.read()

            #We need to enable the /listSpecies resource with no limitis
            elif self.path.startswith("/listSpecies") and self.path.endswith("/listSpecies"):

                try:
                    server = "http://rest.ensembl.org"
                    ext = "/info/species?"

                    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    data_species = r.json()

                    # We can check that the species will be in this key calles "species".
                    # Check at: http://rest.ensembl.org/info/species?content-type=application/json

                    species = data_species["species"]

                    # List for common names
                    species_common_list = []

                    # List for original names
                    species_name_list = []

                    # We get the common name from every species and we create a list with these names

                    for element in range(len(species)):
                        species_common_list.append(species[element]["common_name"])
                        species_name_list.append(species[element]["name"])

                    species_elements = []

                    # First element of species_name_list corresponds to first element of species_common_list so we enumerate the first and work with both of them
                    for num, element in enumerate(species_name_list):
                        # We are appending to species_elements list all the elements we are going to send
                        normal_name = '{}. Normal: {}'.format(num + 1, species_name_list[num])
                        species_elements.append(normal_name)
                        common_name = 'Common: {}'.format(species_common_list[num])
                        species_elements.append(common_name)

                    # <br> in order to make line breaks when we put the information into the code of the HTML response
                    species_result = '<br>'.join(species_elements)

                    # HTML response page
                    contents = """
                                         <!DOCTYPE html>
                                         <html lang="en" dir="ltr">
                                           <head>
                                             <meta charset="utf-8">
                                             <title>SPECIES PAGE</title>
                                           </head>
                                           <body style="background-color: lightyellow;">
                                             <h1>WELCOME TO THE SPECIES PAGE</h1>
                                             <p> The available species in the ensambl database are: </p>
                                             <p> {} </p>
                                             <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                                           </body>
                                         </html>""".format(species_result)
                    # Exceptions to redirect the user to the error html page if something goes wrong
                    # (wrong request, empty request, wrong type or values for request)

                except ValueError:
                    f = open('error.html', 'r')
                    contents = f.read()
                    f.close()

                except IndexError:
                    f = open('error.html', 'r')
                    contents = f.read()
                    f.close()

                except requests.HTTPError:
                    f = open('error.html', 'r')
                    contents = f.read()
                    f.close()

            # Now, we go with the endpoints:

            elif self.path.startswith("/listSpecies") or self.path.startswith("/karyotype") or  self.path.startswith("/chromosomeLength") or self.path.startswith("/geneSeq") or self.path.startswith("/geneInfo") or self.path.startswith("/geneCalc") or self.path.startswith("/geneList"):

                # Now we are going to make a list from the path in order to be able to work with different resources
                resource_list = self.path.split("?", 1)
                resource_list = resource_list[1]
                form_list = resource_list.split("=", 1)

                # form_list[0] allows us to get the first parameter of our path and then work with different responses depending on the resources

                if self.path.startswith("/listSpecies"):

                    try:
                        # Has the client set a limit?

                        limit = form_list[1]

                        plus_list = []

                        # Eliminate wrong introduced spaces
                        for i in limit:
                            if i != "+":
                                plus_list.append(i)

                        limit = ''.join(plus_list)

                        # LIST OF AVAILABLE SPECIES: We get the information about the server from the ensemble api documentation

                        server = "http://rest.ensembl.org"
                        ext = "/info/species?"

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        data_species = r.json()

                        # We can check that the species will be in this key calles "species". Check at: http://rest.ensembl.org/info/species?content-type=application/json
                        species = data_species["species"]

                        # List for common names
                        species_common_list = []

                        # List for original names
                        species_name_list = []

                        # We get the common name from every species and we create a list with these names
                        for element in range(len(species)):
                            species_common_list.append(species[element]["common_name"])
                            species_name_list.append(species[element]["name"])

                        # If the limit is different to (empty) then we convert the input limit into an integer
                        if limit !='':

                            limit = int(limit)

                        # If the limit exceeds the length of the list, we convert the input limit into the length of the list so as to not arise any error
                            if limit > len(species_name_list):
                                limit = len(species_name_list)

                            # We cut the lists according to the established limits
                            species_name_list = species_name_list[:limit]
                            species_common_list = species_common_list[:limit]

                        species_elements =[]

                        # First element of species_name_list corresponds to first element of species_common_list so we enumerate the first and work with both of them
                        for num, element in enumerate(species_name_list):

                            # We are appending to species_elements list all the elements we are going to send
                            normal_name = '{}. Normal: {}'.format(num +1, species_name_list[num])
                            species_elements.append(normal_name)
                            common_name ='Common: {}'.format(species_common_list[num])
                            species_elements.append(common_name)

                        # <br> in order to make line breaks when we put the information into the code of the HTML response
                        species_result = '<br>'.join(species_elements)

                        # HTML response page
                        contents = """
                        <!DOCTYPE html>
                        <html lang="en" dir="ltr">
                          <head>
                            <meta charset="utf-8">
                            <title>SPECIES PAGE</title>
                          </head>
                          <body style="background-color: lightyellow;">
                            <h1>WELCOME TO THE SPECIES PAGE</h1>
                            <p> The available species in the ensambl database are: </p>
                            <p> {} </p>
                            <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                          </body>
                        </html>""".format(species_result)

                    # Exceptions to redirect the user to the error html page if something goes wrong
                    # (wrong request, empty request, wrong type or values for request)
                    except ValueError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except IndexError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except requests.HTTPError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                elif self.path.startswith("/karyotype"):

                    # It's possible that the species does not exit, so we make a try/except to avoid arising errors

                    try:

                        """
                        Our first endpoint, listSpecies, only had one parameter, so we could work with the form_list, in
                        this case we have more than one parameter so we have to make a second_list that gives us the 
                        introduces parameters as its elements.
                        
                        """

                        second_list = resource_list.split(("&"))
                        for element in range(len(second_list)):
                            second_list[element] = second_list[element].split('=')
                            second_list[element] = second_list[element][1]

                            # If we introduce the species homo sapiens, in the url it will be seen as homo+sapiens
                            # We need to redefine these kind of parameters and remove the '+' symbol
                            symbol = '+'
                            if symbol in second_list[element]:
                                second_list[element] = second_list[element].split(symbol)
                                only_element = ' '.join(second_list[element])
                                only_element = only_element.strip()
                                second_list[element] = only_element

                        introduced_species = second_list[0]

                        server = "http://rest.ensembl.org"

                        ext = "/info/assembly/" + introduced_species

                        #Request to the api documentation of ensembl
                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        data_karyotype = r.json()

                        karyotype = data_karyotype["karyotype"]

                        emptyness = []

                        # Some species do not have this information available, so the result of karyotype will be an empty list
                        # This means that the species is in the data base, but we don't have this information

                        if karyotype == emptyness:
                            karyotype.append('No info available for species {}'.format(introduced_species))

                        # We join them with breaklines <b> so the user can see it pretty printed in the HTML
                        karyotype_result = '<br>'.join(karyotype)

                        # HTML response page
                        contents = """
                        <!DOCTYPE html>
                        <html lang="en" dir="ltr">
                          <head>
                            <meta charset="utf-8">
                            <title>KARYOTYPE PAGE</title>
                          </head>
                          <body style="background-color: lightyellow;">
                            <h1>WELCOME TO THE KARYOTYPE PAGE</h1>
                            <p> The karyotype of the species {}: </p>
                            <p> {} </p>
                            <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                          </body>
                        </html>""".format(introduced_species, karyotype_result)

                    # If the species information requested is not available, instead of arising the error, we redirect the user to an error page (personalized for this error)
                    except requests.HTTPError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except IndexError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except ValueError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                elif self.path.startswith("/chromosomeLength"):


                    try:
                        # Transform the request path into something we can work with
                        # Ex: transform sequence=homo+sapiens&operation=karyotype into ['homo sapiens', 'karyotype']

                        second_list = resource_list.split('&')

                        for element in range(len(second_list)):
                            second_list[element] = second_list[element].split('=')
                            second_list[element] = second_list[element][1]

                            symbol = '+'
                            if symbol in second_list[element]:
                                second_list[element] = second_list[element].split(symbol)
                                only_element = ' '.join(second_list[element])
                                only_element = only_element.strip()
                                second_list[element] = only_element

                        # The result will be the same if we write http://localhost:8000/chromosomeLength?chromo=4&specie=horse than
                        # if we wrote http://localhost:8000/chromosomeLength?specie=horse&chromo=4
                        if form_list[0] == "specie":
                            introduced_species = second_list[0]
                            chromo = second_list[1]

                        else:
                            introduced_species = second_list[1]
                            chromo = second_list[0]

                        chromo = chromo.upper()

                        server = "http://rest.ensembl.org"

                        ext = "/info/assembly/" + introduced_species

                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        # Import the data
                        data_karyotype = r.json()

                        # Create an empty list
                        len_list = []

                        """
                        The top level region of the json dictionary we obtain (data_karyotype) contains the chromosomes 
                        with information relevant to them such as the name, the coord_system and the length. We want the 
                        name and length.

                        The for loop serves us to go accross this top level region and find the name of the chromosome 
                        which is equal to the one requested.

                        Then we obtain the name and the length of this chromosome.
                        """

                        for element in range(len(data_karyotype["top_level_region"])):
                            if data_karyotype["top_level_region"][element]["name"] == chromo:
                                element_list = []
                                element_list.append(data_karyotype["top_level_region"][element]["name"])
                                element_list.append(data_karyotype["top_level_region"][element]["length"])
                                len_list.append(element_list)


                        """
                        Now, we have in our len_list the name and the length of the chromosome and we are going to 
                        create a list with the results but with the complete string. If this result list is empty, it means
                        that the info is not available. The chromosome does not exist for that species or it's not in 
                        the data base.
                        """

                        results_len = []

                        for element in range(len(len_list)):
                            if len_list[element][0] == chromo:
                                element_str = "Length of the chromosome {} is: {}".format(len_list[element][0],len_list[element][1])
                                results_len.append(element_str)

                        emptyness = []

                        if results_len == emptyness:
                            results_len.append('No chromosome info found')

                        len_result = '<br>'.join(results_len)

                        # HTML response page
                        contents = """
                       <!DOCTYPE html>
                       <html lang="en" dir="ltr">
                         <head>
                           <meta charset="utf-8">
                           <title>CHROMOSOME LENGTH PAGE</title>
                         </head>
                         <body style="background-color: lightyellow;">
                           <h1>WELCOME TO THE CHROMOSOME LENGTH PAGE</h1>
                           <p> The chromosome length of the chromosome {} for species {}: </p>
                           <p> {} </p>
                           <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                         </body>
                       </html>""".format(chromo, introduced_species, len_result)

                    # If the species information requested is not available, instead of arising the error, we redirect the user to an error page (personalized for this error)
                    except requests.HTTPError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except IndexError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except ValueError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                elif self.path.startswith("/geneSeq"):

                    try:
                        gen_name = form_list[1]

                        plus_list = []

                        # Eliminate wrong introduced spaces
                        for i in gen_name:
                            if i != "+":
                                plus_list.append(i)

                        gen_name = ''.join(plus_list)

                        gen_name = gen_name.upper()

                        final_name = gen_name

                        server = "http://rest.ensembl.org"

                        """"
                        The user can introduce two types of data:
                        (1) Id
                        (2) Symbol
                        Depending on the way the user introduces the gen, the request to obtain the info will be different.
                        If the user introduces the symbol, we first need to find which id corresponds to the symbol and 
                        then find the sequence.
                        If the user introduces the id we can obtain the sequence directly.
                        Since the genes id start with 'ENSG' we will use this info as a condition.
                        """

                        if gen_name.startswith("ENSG"):
                            gen_name = gen_name

                        else:

                            #Request to the API documentation to find the ID of the given gen in form of symbol
                            server = "https://rest.ensembl.org"
                            ext = "/xrefs/symbol/homo_sapiens/" + gen_name + "?"

                            r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()

                            decoded = r.json()
                            gen_name = decoded[0]["id"]


                        gen_name = gen_name + "?"

                        ext = "/sequence/id/" + gen_name

                        #This time, the request is for the sequence
                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        decoded = r.json()

                        #The sequence is just the value of the key "sequence" of the dictionary
                        seq_basis = decoded["seq"]

                        contents = """
                       <!DOCTYPE html>
                       <html lang="en" dir="ltr">
                         <head>
                           <meta charset="utf-8">
                           <title>GEN SEQUENCE PAGE</title>
                         </head>
                         <body style="background-color: lightyellow;">
                           <h1>WELCOME TO THE GEN SEQUENCE PAGE</h1>
                           <p> The sequence of the gen {} is: </p>
                           <p> {} </p>
                           <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                         </body>
                       </html>""".format(final_name, seq_basis)

                    except ValueError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except IndexError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except requests.HTTPError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                elif self.path.startswith("/geneInfo"):

                    try:
                        gen_name = form_list[1]

                        plus_list = []

                        # Eliminate wrong introduced spaces
                        for i in gen_name:
                            if i != "+":
                                plus_list.append(i)

                        gen_name = ''.join(plus_list)

                        gen_name = gen_name.upper()

                        """"
                        The user can introduce two types of data:
                        (1) Id
                        (2) Symbol
                        Depending on the way the user introduces the gen, the request to obtain the info will be different.
                        If the user introduces the symbol, we first need to find which id corresponds to the symbol and 
                        then find the sequence.
                        If the user introduces the id we can obtain the sequence directly.
                        Since the genes id start with 'ENSG' we will use this info as a condition.
                        """
                        #The result of the request is quite simmilar from one type to another, but we must specify the conditions anyways
                        if gen_name.startswith("ENSG"):

                            gen_name = gen_name + '?'
                            server = "https://rest.ensembl.org"
                            ext = "/lookup/id/" + gen_name

                            r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()

                            decoded = r.json()

                            #ID of the gen
                            id = decoded["id"]
                            #Symbol of the gen
                            display_name = decoded["display_name"]
                            #Start position
                            start = decoded["start"]
                            #End position
                            end = decoded["end"]
                            #Chromosome where the gen resides
                            chromosome = decoded["seq_region_name"]

                        else:

                            gen_name = gen_name + '?'
                            server = "https://rest.ensembl.org"
                            ext = "/lookup/symbol/homo_sapiens/" + gen_name

                            r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()

                            decoded = r.json()

                            id = decoded["id"]
                            display_name = decoded["display_name"]
                            start = decoded["start"]
                            end = decoded["end"]
                            chromosome = decoded["seq_region_name"]

                        ext = "/sequence/id/" + id + '?'

                        #We also request sequence to know the length of the gen sequence
                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        decoded = r.json()
                        seq_5 = decoded["seq"]
                        length_sequence = len(seq_5)

                        contents = """
                       <!DOCTYPE html>
                       <html lang="en" dir="ltr">
                         <head>
                           <meta charset="utf-8">
                           <title>GEN INFO PAGE</title>
                         </head>
                         <body style="background-color: lightyellow;">
                           <h1>WELCOME TO THE GEN INFO PAGE</h1>
                           <p> GEN ID: {} </p>
                           <p> GEN SYMBOL: {}</p>
                           <p> GEN SEQUENCE LENGTH: {}</p>
                           <p> CHROMOSOME WHERE THE GEN RESIDES: {}</p>
                           <p> START: {} </p>
                           <p> END: {} </p>
                           <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                         </body>
                       </html>""".format(id, display_name, length_sequence, chromosome, start, end)

                    except IndexError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except ValueError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except requests.HTTPError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                elif self.path.startswith("/geneCalc"):

                    try:

                        gen_name = form_list[1]

                        plus_list = []

                        # Eliminate wrong introduced spaces
                        for i in gen_name:
                            if i != "+":
                                plus_list.append(i)

                        gen_name = ''.join(plus_list)

                        gen_name = gen_name.upper()

                        #Name of the gen(if the user introduced the ID, the ID, and if the user introduced the symbol, the symbol)
                        final_name = gen_name

                        server = "http://rest.ensembl.org"

                        """"
                        The user can introduce two types of data:
                        (1) Id
                        (2) Symbol
                        Depending on the way the user introduces the gen, the request to obtain the info will be different.
                        If the user introduces the symbol, we first need to find which id corresponds to the symbol and 
                        then find the sequence.
                        If the user introduces the id we can obtain the sequence directly.
                        Since the genes id start with 'ENSG' we will use this info as a condition.
                        """

                        if gen_name.startswith("ENSG"):
                            gen_name = gen_name

                        else:

                            server = "https://rest.ensembl.org"
                            ext = "/xrefs/symbol/homo_sapiens/" + gen_name + "?"

                            #Request to get the ID in case the user introduces the symbol
                            r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()

                            decoded = r.json()
                            gen_name = decoded[0]["id"]

                        gen_name = gen_name + "?"

                        ext = "/sequence/id/" + gen_name

                        #Request to get the sequence of the gen
                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        decoded = r.json()

                        seq_basis = decoded["seq"]

                        #Instance of class Seq created
                        seq_6 = Seq(seq_basis)
                        #Calculations with methods of Seq class we imported
                        total_length = seq_6.len()
                        per_a = seq_6.perc('A')
                        per_c = seq_6.perc('C')
                        per_g = seq_6.perc('G')
                        per_t = seq_6.perc('T')

                        contents = """
                       <!DOCTYPE html>
                       <html lang="en" dir="ltr">
                         <head>
                           <meta charset="utf-8">
                           <title>GEN INFO PAGE</title>
                         </head>
                         <body style="background-color: lightyellow;">
                           <h1>WELCOME TO THE GEN CALCULATIONS PAGE</h1>
                           <p> GEN NAME: {} </p>
                           <p> GEN SEQUENCE LENGTH: {}</p>
                           <p> PERCENTAGE {}</p>
                           <p> PERCENTAGE {} </p>
                           <p> PERCENTAGE {} </p>
                           <p> PERCENTAGE {} </p>
                           <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                         </body>
                       </html>""".format(final_name, total_length, per_a, per_c, per_g, per_t)

                    except IndexError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except ValueError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except requests.HTTPError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                elif self.path.startswith("/geneList"):

                    try:

                        second_list = resource_list.split(("&"))

                        for element in range(len(second_list)):
                            second_list[element] = second_list[element].split('=')
                            second_list[element] = second_list[element][1]

                            symbol = '+'
                            if symbol in second_list[element]:
                                second_list[element] = second_list[element].split(symbol)
                                only_element = ' '.join(second_list[element])
                                only_element = only_element.strip()
                                second_list[element] = only_element

                        chromosoma = second_list[0]

                        start = second_list[1]

                        end = second_list[2]

                        server = "http://rest.ensembl.org"

                        ext_1 = "/overlap/region/human/"
                        ext_2 = "?feature=gene;content-type=application/json"

                        ext = ext_1 + chromosoma + ':' + start + ':' + end + ext_2

                        #Request to know the genes in a certain region of a given chromosome
                        r = requests.get(server + ext, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        #Dictionary of genes
                        decoded = r.json()

                        #Create an empty list
                        genes_list = []

                        """
                        For each element of the dictionary, this is, for each gene, we will add to gen_list the name, id,
                        and the description of the gene, then we will add this list to the genes_list
                        
                        """

                        for i in range(len(decoded)):
                            gen_list = []
                            gen_list.append(decoded[i]["external_name"])
                            gen_list.append(decoded[i]["id"])
                            gen_list.append(decoded[i]["description"])
                            genes_list.append(gen_list)


                        #Now we make a list of results in order to print the genes in a pretty way later

                        result = []

                        for num, element in enumerate(genes_list):
                            id_name = "{}. ID: {}".format(num + 1, genes_list[num][1])
                            result.append(id_name)
                            symbol_name = "Symbol: {}".format(genes_list[num][0])
                            result.append(symbol_name)
                            description = "Description: {}<br>".format(genes_list[num][2])
                            result.append(description)

                        #Join the result list with <br> so it shows break lines in the HTML response
                        final = '<br>'.join(result)

                        contents = """
                       <!DOCTYPE html>
                       <html lang="en" dir="ltr">
                         <head>
                           <meta charset="utf-8">
                           <title>CHROMOSOME REGION PAGE</title>
                         </head>
                         <body style="background-color: lightyellow;">
                           <h1>WELCOME TO THE CHROMOSOME REGION PAGE</h1>
                           <p> CHROMOSOME: {} </p>
                           <p> START POSITION: {}</p>
                           <p> END POSITION: {}</p>
                           <p> GENES:</p>
                           <p> {} </p>
                           <p><a href="http://localhost:8000/"> Click here to go to the home page</a></p>
                         </body>
                       </html>""".format(chromosoma, start, end, final)

                    except IndexError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except ValueError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                    except requests.HTTPError:
                        f = open('error.html', 'r')
                        contents = f.read()
                        f.close()

                #If the first element after the endpoint is wrong it will show the HTML error response
                else:
                    f = open('error.html', 'r')
                    contents = f.read()
                    f.close()

            #If the endpoint is different from the valid ones
            else:

                f = open('error.html', 'r')
                contents =f.read()
                f.close()

        except IndexError:
            f = open('error.html', 'r')
            contents = f.read()
            f.close()

        except ValueError:
            f = open('error.html', 'r')
            contents = f.read()
            f.close()

        except requests.HTTPError:
            f = open('error.html', 'r')
            contents = f.read()
            f.close()


        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler

Handler = TestHandler

#Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("MEDIUM SERVER")
    print("Serving at PORT", PORT)

    #Main loop: attend the client. Whenever there is a new client, the handler is called

    try:
        socketserver.TCPServer.allow_reuse_address = True
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")