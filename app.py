import streamlit as st
import networkx as nx
from pyvis.network import Network
from PIL import Image
import matplotlib.pyplot as plt

def is_graph_possible(sequence):
    result = False
    # Convert the sequence to a list and sort it in descending order
    sequence = list(sequence)
    sequence.sort(reverse=True)
    runtime = 1
    st.caption("Description:")
    while sequence:
        
        # Print the current sequence
        st.write(f"Step {runtime}: Sorted graph sequence as: {tuple(sequence)}")

        # Remove the first element
        first = sequence.pop(0)
        # print(f"Removed the first element: {first} => {tuple(sequence)}")
        # print(f"Subtracted 1 from the first 2 elements, with result: {first} => {tuple(sequence)}")


        # Print the sequence in a more readable format
        if len(sequence) <= 1:
            st.write(f"Removed the first element: {first} => ({sequence[0]})")
        else:
            print(f"Removed the first element: {first} => {tuple(sequence)}")

        # Check if there are enough elements left to subtract from
        if first > len(sequence):
            st.write(f"Not enough elements in the rest of the sequence {tuple(sequence)}")
            st.write(f"At least {first} elements are required at this moment => It is NOT POSSIBLE to build a graph from the given input sequence!")
            return

        # Subtract 1 from the first 'first' elements
        for i in range(first):
            sequence[i] -= 1

        if len(sequence) <= 1:
          st.write(f"Subtracted 1 from the first elements: => {sequence[0]}")
        else:
            st.write(f"Subtracted 1 from the first elements: => {tuple(sequence)}")

        # Remove all zero elements
        sequence = [i for i in sequence if i != 0]

        # Sort the sequence in descending order again
        sequence.sort(reverse=True)
        runtime = runtime + 1
    st.write("The rest of the sequence contains only zero values => It is POSSIBLE to build a graph from the given input sequence!")
    return True
# Test the function
# sequence = (1,1,1,1)
# is_graph_possible(sequence)


def draw_graph_pyvis(G):
  """
  This function displays the constructed graph using PyVis.

  Args:
      G: A NetworkX graph object representing the graph to visualize.
  """

  if G is None:
    st.write("Failed to construct a graph from the sequence.")
    return

  # Create a PyVis network object
  vis = Network(height="700px", width="100%")

  # Add nodes with labels from node indices
  for node, degree in G.nodes(data=True):
    vis.add_node(node, label=str(node), title=f"Degree: {degree}")

  # Add edges between nodes
  for edge in G.edges():
    vis.add_edge(edge[0], edge[1])

  # Customize node and edge styles (optional)
  vis.barnes_hut_layout()
  vis.stabilization_iterations = 500  # Adjust for better stabilization

  st.write(vis)  # Display the PyVis network

def draw_graph_streamlit(z):
    """
    This function displays the constructed graph using Streamlit.

    Args:
        G: A NetworkX graph object representing the graph to visualize.
    """

    # Specify seed for reproducibility
    seed = 0
    # z = [6,6,5,4,3,3,3,3,2,1]
    # st.write(f"Is the degree sequence graphical? {nx.is_graphical(z)}")

    # st.write("Configuration model")
    G = nx.configuration_model(z, seed=seed)  # configuration model, seed for reproducibility

    # Check if the graph is connected
    # st.write(f"Is the graph connected? {nx.is_connected(G)}")

    degree_sequence = [d for n, d in G.degree()]  # degree sequence
    # st.write(f"Degree sequence {degree_sequence}")
    # st.write("Degree histogram")
    hist = {}
    for d in degree_sequence:
        if d in hist:
            hist[d] += 1
        else:
            hist[d] = 1
    # st.write("degree #nodes")
    # for d in hist:
    #     st.write(f"{d:4} {hist[d]:6}")

    # Draw the graph
    pos = nx.spring_layout(G, seed=seed)  # Seed layout for reproducibility
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos=pos)
    st.pyplot(plt)

st.title("Graph Score Validation and Visualization")
st.subheader("- Phuc Long Project 🏆 🐲 ")

# Get user input for the degree sequence
sequence_str = st.text_input("Enter a degree sequence (comma-separated integers):")

if sequence_str:
  try:
    sequence = [int(x) for x in sequence_str.split(",")]
  except ValueError:
    st.error("Invalid input: Please enter comma-separated integers.")
  else:
    if is_graph_possible(sequence):
    #   possible_graph = construct_possible_graph(sequence)
      st.success("Valid graph score sequence.")
      if True:
        st.subheader("One Possible Graph:")
        # draw_graph_pyvis(possible_graph)
        draw_graph_streamlit(sequence)
      else:
        st.write("Failed to construct a graph from the sequence.")
    else:
      st.error("Invalid graph score sequence.")



