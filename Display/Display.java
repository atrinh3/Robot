//This is mostly pseudocode for now
import java.util.Scanner;

// Object class for displaying an order.
public class Order {
    private String customer;
    private String flavor;
    private boolean readyStatus;
    private int orderNumber;

    public Order() {
        this.customerName = "";
        this.orderFlavor = "";
        this.orderStatus = 0;
        this.orderNumber = null;
    }

    public String getCustomerName() {
        return this.customerName;
    }

    public void setCustomerName(String name) {
        this.customerName = name;
    }

    public String getOrderFlavor() {
        return this.orderFlavor;
    }

    public String setOrderFlavor(String flavor) {
        this.orderFlavor = flavor;
    }

    public void putInWork() {
        this.orderStatus = 1;
    }

    public void readyOrder() {
        this.orderStatus = 2;
    }

    public void orderPickedUp() {
        this.orderStatus = 4;
    }

    public String getStatus() {
        if (this.orderStatus == 0) {
            return "In queue";
        } else if (this.orderStatus == 1) {
            return "In work!";
        } else {
            return "Order is ready!!";
        }
    }

    public void setStatus(int status) {
        this.orderStatus = status;
    }

    public int getOrderNumber() {
        return this.orderNumber;
    }

    public void setOrderNumber(int num) {
        this.orderNumber = num;
    }
}


public Order interpretLineData(String[] lineData, int orderNum) {
    Order order = new Order();
    Scanner parser = new Scanner(lineData);
    parser.useDelimiter(",");
    int index = 0;
    while parser.hasNext() {
        String value = parser.next();
        switch (index) {
            case 0:
                order.setCustomerName(value);
            case 1:
                order.setOrderFlavor(value);
            case 2:
                order.setStatus(value);
        }
        index++;
    }
    order.setOrderNumber(orderNum);
    return order;
}
    

public List<Order> void updateDisplayData() {
    List<Order> orderList = new ArrayList<Order>();
    try (Scanner scanner = new Scanner(new File(orderCSVFilename));) {
        int orderNumber = 0;
        while (scanner.hasNextLine()) {
            orderList.add(interpretLineData(scanner.nextLine()), orderNumber);
            orderNumber++;
        }
    }
    return orderList;
}

public static void display(List<Order> oList) {
    for (int i = 0; i >= oList.size(); i++) {
        
        displayShow(order.getOrderNumber());
        displayShow(order.getCustomerName());
        displayShow(order.getOrderFlavor());
        displayShow(order.getStatus(), end=true);
    }
}

public static void main(String[] args) {
    while true {
        List<Order> orderList = updateDisplayData(orderList)
        display(orderList);
    }
}

