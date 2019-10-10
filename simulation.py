import random
import sys
from person import Person
from logger import Logger
from virus import Virus
random.seed(42)


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    # (finished) TODO: move defaulted variable class to the end (After virus)
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.pop_size = pop_size # Int
        self.next_person_id = 1 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.newly_infected = []
        self.save_from_vac = 0
        # self.newly_dead = [] # To return newly dead perons
        self.population = self._create_population(self.initial_infected) # List of Person objects, this is created right after calling simulation class

        self.file_name = "_virus_name_{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            self.virus.name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)


    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.
        
        population = []

        # Infect to population
        for _ in range(self.initial_infected):
            infected_person = Person(self.next_person_id, False, self.virus) # Creating a Person object
            self.next_person_id += 1
            population.append(infected_person)

        #  Vaccinated
        for _ in range(int(self.vacc_percentage * self.pop_size)):
            vaccinated_person = Person(self.next_person_id, True)
            self.next_person_id += 1
            population.append(vaccinated_person)

        #  Unvaccinated
        for _ in range(self.pop_size - self.initial_infected - int(self.vacc_percentage * self.pop_size)):
            unvaccinated_person = Person(self.next_person_id, False)
            self.next_person_id += 1
            population.append(unvaccinated_person)

        return population

    def print_pop(self):
        print(self.population)
        print(len(self.population))
        print(self.initial_infected)
        print(self.vacc_percentage)

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.
        # Check if all are dead
        # if self.total_dead == self.pop_size:
        #     return False

        # Count alive vaccinated people
        vaccinated = 0
        for person in self.population:
            if person.is_alive and person.is_vaccinated:
                vaccinated += 1

        # # Check if all people are vaccinated
        # if vaccinated == self.pop_size - self.total_dead:
        #     return False
        
        # return True
        # print(vaccinated)
        # print(self.total_dead)
        # print(vaccinated + self.total_dead)

        if (vaccinated + self.total_dead) >= self.pop_size:
            return False
        else:
            return True

        # if self.current_infected == 0:
        #     return False
        # else:
        #     return True


    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper

        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        while should_continue:
            # print("test")
            self.time_step()
            time_step_counter += 1
            self._infect_newly_infected()
            should_continue = self._simulation_should_continue()
            self.logger.log_time_step(time_step_counter, self.total_dead, self.total_infected)
            # self.logger.log_time_step(time_step_counter)
            # should_continue = self._simulation_should_continue

        print(f"The simulation has ended after {time_step_counter} turns.")
        self.logger.log_percentage(self.pop_size, self.total_dead, self.total_infected, self.save_from_vac)

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.
        interaction_count = 0
        for person in self.population:
            if person.infection == self.virus and person.is_alive:
                while interaction_count < 100:
                    random_person = random.choice(self.population)
                    if random_person.is_alive and random_person._id != person._id:
                        interaction_count += 1
                        self.interaction(person, random_person)
                    # print(interaction_count)
                interaction_count = 0
        #         if person.did_survive_infection():
        #             self.logger.log_infection_survival(person, False)
        #         else:
        #             self.total_dead += 1
        #             self.logger.log_infection_survival(person, True)

        for person in self.population:
            if person.is_alive and person.infection:
                if person.did_survive_infection():
                    self.logger.log_infection_survival(person, False)
                # Else Person dies
                else:
                    self.logger.log_infection_survival(person, True)
                    self.total_dead += 1

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.

        # if random_person.is_vaccinated or random_person.infection:
        
        if random_person.is_vaccinated is True:
            self.save_from_vac += 1
            self.logger.log_interaction(person, random_person, None, True, None)
        elif random_person.infection is not None:
            self.logger.log_interaction(person, random_person, True, None, None)
        else:
            if random.random() <= self.virus.repro_rate:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, None, None, True)
            else:
                self.logger.log_interaction(person, random_person)
        
        # virus_defense_0 = random.uniform(0.0, 1.0)

        # if virus_defense_0 < virus.repro_rate:
        #     random_person.infection = True
        #     self.newly_infected.append(random_person._id)
        #     self.logger.log_infection_survival(person, random_person)
        # elif virus_defense_0 > virus.repro_rate:
        #     random_person.infection = False


    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.

        for person in self.population:
            for id in self.newly_infected:
                if person._id == id:
                    person.infection = self.virus
                    self.total_infected += 1
                    self.current_infected += 1
        self.newly_infected  = []

# if __name__ == "__main__":
#     params = sys.argv[1:]
#     virus_name = str(params[2])
#     repro_num = float(params[3])
#     mortality_rate = float(params[4])

#     pop_size = int(params[0])
#     vacc_percentage = float(params[1])

#     if len(params) == 6:
#         initial_infected = int(params[5])
#     else:
#         initial_infected = 1

#     virus = Virus(virus_name, repro_num, mortality_rate)
#     sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

#     sim.run()

virus = Virus("Ebola", 0.90, 0.25)
sim = Simulation(250, .90, virus, 10)
sim.run()

# virus2 = Virus("Diphtheria", 0.60, 0.08)
# sim2 = Simulation(5000, .88, virus2, 10)
# sim2.run()